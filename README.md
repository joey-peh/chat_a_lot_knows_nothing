# Chat-a-Lot Knows Nothing

## Problem Statement

As a software engineer, I spend endless hours reading UCS documentation, but I often forget the basics of key financial terms because the volume of material is overwhelming. 

There are countless documents to sift through, yet all I really want is to ask a domain expert (SME) simple, direct questions like:

> “What exactly is a provable debt?”

Instead of spending valuable time digging through dense documentation, I'd rather get a quick, reliable answer and refocus on the engineering work that actually moves the needle.

## My Solution

A chatbot that:

- Lets me upload documents for the model to understand  
- Prioritises knowledge directly from the uploaded documents  
- Raises no privacy concerns  
- Answers simple questions like “What is provable debt?” in just seconds

## Architecture

- **UI**  
  Streamlit

- **Orchestration Layer**  
  Django + LangGraph

- **Data & Knowledge Base**  
  PostgreSQL / ChromaDB (vector) / Pinecone (vector)

- **Model & Integration Layer**  
  Ollama / LM Studio / GGUF models v ia llama.cpp.. still deciding

- **Deployment**  
  [to be specified]

- **Hosting**  
  [to be specified]
