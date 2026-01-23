# Docker Setup

This project uses Docker Compose to run both the Django backend and Streamlit frontend with a PostgreSQL database.

## Prerequisites

- Docker
- Docker Compose

## Setup

1. **Configure environment variables:**
   - Update the `.env` file in the root directory with your OpenAI API key:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

2. **Build and run containers:**
   ```bash
   docker-compose up --build
   ```

   Or to run in background:
   ```bash
   docker-compose up -d --build
   ```

3. **Access the services:**
   - Frontend (Streamlit): http://localhost:8501
   - Backend API: http://localhost:8000
   - Database: localhost:5432

## Available Commands

- **Start services:**
  ```bash
  docker-compose up
  ```

- **Stop services:**
  ```bash
  docker-compose down
  ```

- **View logs:**
  ```bash
  docker-compose logs -f
  ```

- **Run migrations:**
  ```bash
  docker-compose exec backend python manage.py migrate
  ```

- **Create superuser:**
  ```bash
  docker-compose exec backend python manage.py createsuperuser
  ```

## Services

### Backend (Django)
- Python 3.12
- Django with DRF
- LangChain & LangGraph integration
- PostgreSQL database
- Runs on port 8000

### Frontend (Streamlit)
- Python 3.12
- Streamlit
- Runs on port 8501

### Database (PostgreSQL)
- PostgreSQL 13
- Stores Django models
- Runs on port 5432

## Environment Variables

The backend reads the `.env` file which should contain:
- `OPENAI_API_KEY`: Your OpenAI API key

## Troubleshooting

- **Port already in use:** Change ports in `docker-compose.yml`
- **Database connection issues:** Ensure PostgreSQL service is running and healthy
- **Permission denied:** Run Docker commands with appropriate permissions

