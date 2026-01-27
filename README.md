# Gemini Multimodal Chatbot

A powerful chatbot application that leverages Google's Gemini models to handle multimodal inputs (text and images). The application is built with a FastAPI backend and a Streamlit frontend.

## Features

- **Multimodal capabilities**: Chat with text and images.
- **RAG (Retrieval-Augmented Generation)**: Ingests documents to provide context-aware answers.
- **FastAPI Backend**: Robust and scalable API.
- **Streamlit Frontend**: User-friendly interface for interacting with the bot.

## Prerequisites

- Python 3.10+
- A Google Cloud Project with Gemini API access.
- API Key for Google Gemini.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd Multimodal-ChatBot
    ```

2.  **Backend Setup:**
    Navigate to the `backend` directory:
    ```bash
    cd backend
    ```
    Create a virtual environment and install dependencies:
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    # source venv/bin/activate
    
    pip install -r requirements.txt
    ```
    Create a `.env` file in the `backend` directory with your credentials (see `.env.example` if available, or ask the developer).

3.  **Frontend Setup:**
    (The frontend dependencies are included in the backend `requirements.txt` for this simple setup, but ensure you have streamlit installed).

## Usage

### 1. Start the Backend Server

From the `backend` directory:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`. API docs at `http://localhost:8000/docs`.

### 2. Start the Frontend Application

Open a new terminal, activate the environment, and run:

```bash
# From backend directory
streamlit run app/frontend/streamlit_app.py
```

The application will open in your browser.

## Project Structure

- `backend/app`: Main application code.
    - `main.py`: Entry point for FastAPI.
    - `routes/`: API endpoints.
    - `core/`: Core logic and configuration.
    - `frontend/`: Streamlit application code.
- `data/`: Directory for storing data (ignored by git).
