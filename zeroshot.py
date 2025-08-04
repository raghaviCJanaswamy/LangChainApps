from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from openai import OpenAI



# Initialize the model
llm = ChatOpenAI(model_name="gpt-4o", temperature=0)

import os
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Define a Zero-Shot Prompt
prompt_template = """
You are a concise assistant.
Summarize the following article in one sentence:
{article}
"""

prompt = PromptTemplate(
    input_variables=["article"],
    template=prompt_template
)

# Create the chain
chain = LLMChain(llm=llm, prompt=prompt)

# Example input
article_text = """
OpenAI has launched a new model called GPT-4o, offering faster responses,
better reasoning, and support for multiple modalities including text, image, and audio.
"""

# Run the chain
response = chain.run(article=article_text)

print("Zero-Shot Response:", response)




