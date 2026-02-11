# Multimodal Chatbot with RAG

This project is a multimodal chatbot that accepts text, images, and documents, retrieves relevant context, and generates grounded responses using large language models. The system combines retrieval-augmented generation (RAG), a FastAPI backend, and a Streamlit interface to support interactive querying.

The goal of this project is to explore how multimodal inputs and retrieval pipelines can improve the accuracy and usefulness of chatbot responses compared to plain LLM prompting.

---

## What This Project Does

The chatbot can:

- Accept text queries  
- Process uploaded files or images  
- Retrieve relevant context from indexed data  
- Generate responses grounded in retrieved information  
- Provide an interactive chat interface for experimentation  

Instead of relying purely on the language model’s memory, the system retrieves relevant information first and uses it to generate answers. This reduces hallucination and improves factual grounding.

---

## System Architecture

High-level flow:

User → Streamlit UI → FastAPI Backend → Retriever → LLM → Response

1. The user submits a query through the Streamlit interface  
2. FastAPI handles the request and routes it to the retrieval pipeline  
3. Relevant context is retrieved from indexed data  
4. The LLM generates an answer using both the query and retrieved context  
5. The response is returned to the UI  

This separation keeps the UI, API, and retrieval logic modular.

---

## Tech Stack

**Backend**
- FastAPI for API routing and service orchestration  

**Frontend**
- Streamlit for an interactive chat interface  

**AI / Retrieval**
- Retrieval-Augmented Generation (RAG)
- Embedding-based retrieval
- Large language model integration  

**Utilities**
- Python for pipeline logic
- Environment variable configuration for API keys and settings  

---

## Project Structure

Multimodal-Chatbot/
│
├── backend/ # FastAPI services and retrieval logic
├── frontend/ # Streamlit UI
├── utils/ # Helper functions and processing logic
├── requirements.txt
└── README.md

yaml
Copy code

---

## How to Run Locally

1. Clone the repository

git clone https://github.com/tarakaram2134/Multimodal-Chatbot.git
cd Multimodal-Chatbot


2. Create a virtual environment

python -m venv venv
source venv/bin/activate


(Windows PowerShell)

venv\Scripts\activate


3. Install dependencies

pip install -r requirements.txt



4. Start the backend

uvicorn main:app --reload



5. Start the frontend

streamlit run app.py

---

## Design Decisions

**FastAPI**  
Chosen for its speed, clean structure, and easy integration with async pipelines.

**Streamlit**  
Used for rapid prototyping of interactive AI interfaces without needing a full frontend framework.

**RAG Pipeline**  
Implemented to reduce hallucinations and improve factual accuracy when answering queries.

**Modular Layout**  
Backend, UI, and utilities are separated to make the system easier to extend.

---

## Possible Improvements

Some directions this project could be extended:

- Persistent vector database (FAISS or ChromaDB)
- Streaming responses for better UX
- Authentication and session memory
- Multi-document context handling
- Deployment using Docker and cloud services

---

## Why I Built This

This project is part of my work exploring practical applications of retrieval-augmented generation and multimodal AI systems. The focus was on building a system that is modular, explainable, and easy to extend rather than just a demo script.

---

## Author

**Taraka Ram Donepudi**  
MS Computer Science  
University of Michigan-Flint  

GitHub: https://github.com/tarakaram2134
