# Chat-a-Lot Knows Nothing

## Problem Statement

As a software engineer, I spend endless hours reading documentation, but I often forget the basics of key financial terms because the volume of material is overwhelming. 

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
  Ollama 

- **Deployment**  
  [to be specified]

- **Hosting**  
  [to be specified]


  ## Summary of the flow
1. User Uploads Document: Document is uploaded via Streamlit UI and saved to the local file system.
2. Text Extraction: The text is extracted from PDFs, Word docs, etc.
3. Ollama Processing: The extracted text is sent to Ollama for AI processing (e.g., prioritization or categorization).
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