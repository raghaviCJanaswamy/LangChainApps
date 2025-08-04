import os
import gradio as gr
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

# Load API Key
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize ChatOpenAI with Security Tools context
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0,
    openai_api_key=OPENAI_API_KEY
)

# Memory to store ongoing chat
memory = ConversationBufferMemory()

# Create a conversation chain with system context
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True
)

# Add context to conversation
system_context = """
You are a Security Tools Expert specializing in:
- Contrast Security (application security, SAST, IAST)
- JFrog Xray (artifact scanning, vulnerability detection)
- DevSecOps best practices
- Integration of security tools into CI/CD pipelines
Answer all questions as a knowledgeable consultant.
"""

# Prime the bot with context
conversation.run(system_context)

# Gradio function
def chat_with_bot(user_input, chat_history):
    response = conversation.run(user_input)
    chat_history.append((user_input, response))
    return chat_history, chat_history

# Build Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("## 🔐 Security Tools Conversational Bot (LangChain + GPT-4o)")
    
    chatbot = gr.Chatbot()
    msg = gr.Textbox(label="Ask about Contrast, JFrog Xray, or other security tools...")
    clear_btn = gr.Button("Clear Chat")
    
    msg.submit(chat_with_bot, [msg, chatbot], [chatbot, chatbot])
    clear_btn.click(lambda: None, None, chatbot)

if __name__ == "__main__":
    demo.launch(share=True)
