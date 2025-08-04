import os
import gradio as gr
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.vectorstores import FAISS
from langchain.vectorstores import Chroma


# Load API key
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# 1️⃣ Load PDFs (Replace with your internal docs)
pdf_paths = [
    "docs/Contrast_agent_docs.pdf",
]

docs = []
for path in pdf_paths:
    loader = PyPDFLoader(path)
    docs.extend(loader.load())

# 2️⃣ Split into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(docs)

# 3️⃣ Create embeddings & FAISS index
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
vectorstore = Chroma.from_documents(chunks, embeddings, persist_directory="./chroma_store")
# vectorstore = FAISS.from_documents(chunks, embeddings)

# 4️⃣ Setup Conversational Retrieval Chain
llm = ChatOpenAI(model="gpt-4o", temperature=0, openai_api_key=OPENAI_API_KEY)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

qa_chain = ConversationalRetrievalChain.from_llm(
    llm,
    retriever=vectorstore.as_retriever(),
    memory=memory
)

# 5️⃣ Gradio chat function
def chat_with_bot(user_input, chat_history):
    response = qa_chain.run(user_input)
    chat_history.append((user_input, response))
    return chat_history, chat_history

# 6️⃣ Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("## Security Docs AI Bot (Contrast + JFrog PDFs)")
    chatbot = gr.Chatbot()
    msg = gr.Textbox(label="Ask about Contrast Security or JFrog Xray...")
    clear_btn = gr.Button("Clear Chat")
    
    msg.submit(chat_with_bot, [msg, chatbot], [chatbot, chatbot])
    clear_btn.click(lambda: None, None, chatbot)

if __name__ == "__main__":
    demo.launch(share=True)
