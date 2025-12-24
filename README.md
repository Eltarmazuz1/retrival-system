# RAG System - Installation & Usage

> **⚠️ IMPORTANT **
>
> **The answers to the specific assignment questions (Design Decisions, etc.) are located in the file [`README.txt`](./README.txt).**
>
*

## Overview
This is a simple RAG (Retrieval Augmented Generation) system that ingests text data, creates embeddings using OpenAI, and allows semantic search via a React frontend.

## Prerequisites
- **Python 3.8+**
- **Node.js & npm**
- **OpenAI API Key**
- **Pinecone API Key**

## Installation

### 1. Backend Setup
Navigate to the backend directory:
```bash
cd backend
```

Install Python dependencies:
```bash
pip install -r requirements.txt
```

Create a `.env` file in the `backend` directory with your API keys:
```
OPENAI_API_KEY=sk-your-openai-key
PINECONE_API_KEY=pc-your-pinecone-key
```

### 2. Frontend Setup
Navigate to the frontend directory:
```bash
cd frontend
```

Install Node.js dependencies:
```bash
npm install
```

## Usage

### 1. Data Ingestion
Before searching, you must ingest the data. This process reads `paragraphs.txt`, generates embeddings, and stores them in your Pinecone index.

```bash
cd backend
python ingest.py
```
*Note: This will process the first 200 paragraphs to minimize API costs.*

### 2. Start the Backend Server
```bash
cd backend
python app.py
```
The backend API will run at `http://127.0.0.1:5000`.

### 3. Start the Frontend Application
Open a new terminal:
```bash
cd frontend
npm run dev
```
The application will be available at `http://localhost:5173`.

## System Architecture
- **Backend:** Flask
- **Frontend:** React (Vite)
- **Embeddings:** OpenAI `text-embedding-3-small`
- **Vector Store:** Pinecone (Serverless) - *Cloud-based vector database for scalability and stability.*
