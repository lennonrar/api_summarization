# API Summarization

API for generating summaries from Wikipedia articles using LLMs.

## Quick Start

### 1. Setup Environment

```bash
cp .env.example .env
# Edit .env and add your HF_TOKEN
```

### 2. Run with Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down
```

The API will be available at:
- http://localhost:8000
- http://localhost:8000/docs (Swagger UI)

### 3. Run Locally (without Docker)

```bash
# Install dependencies
poetry install

# Start database (Docker)
docker-compose up -d postgres

# Run migrations
poetry run alembic upgrade head

# Start API
poetry run uvicorn app.main:app --reload
```

## Running Tests

### All Tests (32 tests)

```bash
# Local
pytest tests/ -v

# Docker
docker-compose exec api pytest tests/ -v
```

## API Endpoints

### Health Check
```bash
curl http://localhost:8000/healthcheck
```

### Get Summary
```bash
curl "http://localhost:8000/api/v1/summary/?url2search=https://en.wikipedia.org/wiki/Python_(programming_language)"
```

### Create Summary
```bash
curl -X POST http://localhost:8000/api/v1/summary/ \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://en.wikipedia.org/wiki/Artificial_intelligence",
    "words_limit": 150
  }'
```

## Docker Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Rebuild
docker-compose build --no-cache

# View logs
docker-compose logs -f api
docker-compose logs -f postgres

# Run migrations
docker-compose exec api alembic upgrade head

# Access database
docker-compose exec postgres psql -U default -d api_summarization

# Shell into API container
docker-compose exec api bash
```

## Database

**Connection Info:**
- Host: localhost
- Port: 5432
- User: default
- Password: summarization_pass
- Database: api_summarization

**Connection String:**
```
postgresql://default:summarization_pass@localhost:5432/api_summarization
```

## Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Hugging Face API Token (required for LLM summarization)
HF_TOKEN=your_huggingface_token_here

# Database Configuration
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=summarization_db
DATABASE_URL=postgresql://postgres:postgres@db:5432/summarization_db

# API Configuration
API_PORT=8000


## Requirements

- Python 3.11+
- Docker & Docker Compose
- Poetry (for local development)
- HuggingFace API Token

```
## HuggingFace Integration

This project uses HuggingFace's Inference API for text summarization.

### Getting Your HF Token

1. **Create Account**: Sign up at [huggingface.co](https://huggingface.co)
2. **Generate Token**:
   - Go to Settings → [Access Tokens](https://huggingface.co/settings/tokens)
   - Click "New token"
   - Give it a name (e.g., "API Summarization")
   - Select "Read" access
   - Click "Generate"
3. **Copy Token**: Add it to your `.env` file as `HF_TOKEN`