# Conversational Bot

## Scope - Contrast Security & Jfrog Xray

- OpenAI API helps query for Contrast Security or X-ray tool
- Langchain refines further on 
    Memory
    Context
    Chaining multiple steps
- Automatically remembner past conversations

## Why choosing LangChain over Conersational Bot

Feature | Open AI API | Lang Chain
------| --------| -------
Feature	| Raw OpenAI API	|LangChain
Conversation Memory	|Manual	|Built-in (multiple types)
Prompt Templates	|Manual	|Structured, reusable
Multi-step Chains	|Manual coding	|Native Chains & Agents
Tool Integration	|Manual API calls|	Plug-and-play tools
Vector Search / RAG	|Manual	|Built-in retrievers & embeddings
Scaling/Orchestration	|Manual	|Framework handles it

## LangChain + RAG (Retrieval-Augmented Generation)

- Use Internal PDF to answer questions

### Process

- Load PDFs
- Tokenization ( Chunk the text)
- Create Embeddings ( Convert the tokens to vector embeddings)
- Store Vectors in Vector DB
- Query the DB
    - user asks a question
    - Bot searches Vector DB for relevant chunks
    - Sends context + question + response to <GPT>
