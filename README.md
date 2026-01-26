# Chat-a-Lot Knows Nothing

## Problem Statement

As a software engineer I spend hours in documentation, yet I still forget basic terms — either due to information overload or because I'm just ramping up on the business context.

I don't want to hunt through hundreds of pages just to answer simple questions like:

> “What font should this text use?”

I’d rather get fast, trustworthy answers so I can focus on the engineering work that actually drives progress.

## My Solution

A chatbot that:

- Supports uploading your business documents (PDFs, docs, etc.)
- Grounds every answer exclusively in those files via secure RAG
- Ensures full privacy: 100% offline, no cloud, no data sharing
- Answers straightforward questions in seconds
- Forgets everything when you want—no unwanted memory

## Architecture

- **UI**  
  Streamlit

- **Orchestration Layer**  
  Django + LangGraph

- **Data & Knowledge Base**  
  PostgreSQL / ChromaDB (vector) / Pinecone (vector)

- **Model & Integration Layer**  
  Ollama 

- **Deployment**  
  [to be specified]

- **Hosting**  
  [to be specified]

### Upcoming Improvements
To improve Ollama processing time:
Migrate from PostgreSQL to ChromaDB for vector storage and retrieval.  
Key change: Avoid chunking and embedding every uploaded document upfront. Instead, identify and retrieve only the single most relevant full document matching the user's query, then send its entire unchunked content directly to Ollama for context and processing.

  ## Summary of the flow (Plan)
1. User Uploads Document: Document is uploaded via Streamlit UI and saved to the local file system.
2. Text Extraction: The text is extracted from PDFs, Word docs, etc.
3. Ollama Processing: The extracted text is sent to Ollama for AI processing.
4. Store Results: Processed data (priority score, tags, etc.) is stored in the database for further querying.
5. Asynchronous Processing: Large documents are handled in the background using Celery.
6. Search and Ranking: Users can search and view documents with prioritized results.

## Setup & Installation

### Option 1: Local Development

#### Prerequisites
- Python 3.12+
- PostgreSQL
- pip/venv

#### Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/joey-peh/chat_a_lot_knows_nothing.git
   cd chat_a_lot_knows_nothing
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   # Backend
   cd backend
   pip install -r requirements.txt
   
   # Frontend
   cd ../frontend
   pip install -r requirements.txt
   cd ..
   ```

4. **Configure environment:**
   - Create `.env` file in the root directory:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

5. **Setup database:**
   ```bash
   cd backend
   python manage.py migrate
   cd ..
   ```

6. **Run services:**
   
   **Terminal 1 - Backend:**
   ```bash
   cd backend
   python manage.py runserver 0.0.0.0:8000
   ```
   
   **Terminal 2 - Frontend:**
   ```bash
   cd frontend
   streamlit run app.py
   ```

7. **Access the application:**
   - Frontend: http://localhost:8501
   - Backend API: http://localhost:8000

### Option 2: Docker (Recommended)

#### Prerequisites
- Docker
- Docker Compose

#### Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/joey-peh/chat_a_lot_knows_nothing.git
   cd chat_a_lot_knows_nothing
   ```

2. **Configure environment:**
   - Create/update `.env` file in the root directory:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

3. **Build and run containers:**
   ```bash
   docker-compose up --build
   ```
   
   Or run in background:
   ```bash
   docker-compose up -d --build
   ```

4. **Access the application:**
   - Frontend: http://localhost:8501
   - Backend API: http://localhost:8000
   - Database: localhost:5432

5. **Useful Docker commands:**
   ```bash
   # View logs
   docker-compose logs -f
   
   # Stop containers
   docker-compose down
   
   # Run migrations
   docker-compose exec backend python manage.py migrate
   
   # Create superuser
   docker-compose exec backend python manage.py createsuperuser
   ```

For more Docker details, see [DOCKER_SETUP.md](DOCKER_SETUP.md)

## API Endpoints

- `POST /api/chats/` - Send a message to the chatbot
- `POST /api/documents/` - Upload a document for processing

## Environment Variables

- `OPENAI_API_KEY` - Your OpenAI API key (required for LLM functionality)
- `DEBUG` - Django debug mode (default: True)
- `DB_NAME` - PostgreSQL database name (default: postgres)
- `DB_USER` - PostgreSQL user (default: postgres)
- `DB_PASSWORD` - PostgreSQL password (default: postgres)
- `DB_HOST` - PostgreSQL host (default: db)