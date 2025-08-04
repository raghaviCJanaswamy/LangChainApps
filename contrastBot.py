import os
import gradio as gr
from openai import OpenAI
from dotenv import load_dotenv

# Load API Key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Function to get response from OpenAI
def chat_with_ai(user_input, chat_history):
    chat_history.append(("User", user_input))
    
    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0,
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": user_input}
        ]
    )
    
    bot_reply = response.choices[0].message.content
    chat_history.append(("Bot", bot_reply))
    
    return chat_history, chat_history

# Gradio Chat Interface
with gr.Blocks() as demo:
    gr.Markdown("## 🤖 Conversational AI Bot (OpenAI GPT-4o)")
    chatbot = gr.Chatbot()
    msg = gr.Textbox(label="Your message")
    clear = gr.Button("Clear Chat")
    
    msg.submit(chat_with_ai, [msg, chatbot], [chatbot, chatbot])
    clear.click(lambda: None, None, chatbot)

if __name__ == "__main__":
    demo.launch(share=True)
