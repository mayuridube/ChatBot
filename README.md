RAG-Based Gradio Application with FAISS and Open-Source LLM

This project demonstrates a Retrieval-Augmented Generation (RAG) pipeline integrated into a Gradio UI. Users can upload documents, store embeddings in a FAISS index, and generate answers to queries using an open-source language model.


Key Features

File Upload: Users can upload PDF and PPTX files through the Gradio interface.

Backend Embedding Storage: Click the "Store Embeddings" button to generate and store text embeddings from uploaded files in FAISS.

Query Generation: Users can type queries and click "Generate Answer" to receive responses from the LLM based on the stored data.

Efficient Document Retrieval: Leveraging FAISS for vector-based similarity search.


Tech Stack :

Python 3.8+

LangChain for document processing

HuggingFace Transformers for LLM and embeddings

FAISS for efficient vector similarity search


Run the Project:

python UI_upload_file_chat_bot.py