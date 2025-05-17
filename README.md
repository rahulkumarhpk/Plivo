# Status Page API

A FastAPI-based backend service for managing status pages, incidents, and service health monitoring.

## Installation Requirements

- Python 3.8+
- Docker Desktop
- PostgreSQL 15
- Git

## Features

- Organization management
- Service status tracking
- Incident management
- Real-time updates via WebSocket
- Authentication using Auth0
- PostgreSQL database integration

## Tech Stack

- FastAPI
- SQLAlchemy
- PostgreSQL
- WebSockets
- Auth0 Integration
- Pydantic

## Setup

1. Clone the repository:
```sh
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
```

2. Create a virtual environment:
```sh
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate  # Windows
```

3. Install dependencies:
```sh
pip install -r requirements.txt
```
```

4. Start PostgreSQL using Docker:
```sh
    # Create a Docker volume for persistent data
    docker volume create pgdata

    # Run PostgreSQL container
    docker run -d \
    --name status-page-db \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=postgres \
    -e POSTGRES_DB=statusdb \
    -p 5432:5432 \
    -v pgdata:/var/lib/postgresql/data \
    postgres:15-alpine

    # Verify the container is running
    docker ps
```

5. Create a `.env` file:
```env
SQLALCHEMY_DATABASE_URI=postgresql://postgres:postgres@localhost:5432/statusdb
AUTH0_DOMAIN=auth0-domain.auth0.com
API_AUDIENCE=api-audience
DEV_MODE=true
TEST_TOKEN=your_test_token_here

WEBSOCKET_PORT=5001
WEBSOCKET_HOST=localhost

MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-specific-password
MAIL_DEFAULT_SENDER=your-email@gmail.com

PROJECT_NAME=Status Page API
```

6. Initialize the database:
```sh
python app/seed_db.py
```

7. Run the application:
```sh
uvicorn app.main:app --reload
```

## API Documentation

Once running, visit:
- http://localhost:8000/docs for Swagger UI
- http://localhost:8000/redoc for ReDoc


## Project Structure

```
Backend/
├── api/
│   └── v1/           # API endpoints
├── core/             # Core functionality
├── db/               # Database models and session
├── models/           # Domain models
├── repositories/     # Data access layer
├── schemas/          # Pydantic models
├── services/         # Business logic
└── websocket/        # WebSocket functionality
```
