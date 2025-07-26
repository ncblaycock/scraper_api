# FastAPI Clean Architecture Application

A FastAPI application following clean architecture principles with PostgreSQL database, Alembic migrations, and JWT authentication.

## Features

- Clean Architecture pattern
- User authentication with JWT tokens
- Three main controllers: Users, Reports, Downloads
- PostgreSQL database with SQLAlchemy ORM
- Alembic database migrations
- Uvicorn ASGI server

## Setup

1. Install dependencies:
```bash
poetry install
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your database credentials
```

3. Run database migrations:
```bash
alembic upgrade head
```

4. Start the application:
```bash
poetry run uvicorn main:app --reload
```

## API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `POST /api/v1/users/register` - User registration
- `POST /api/v1/users/login` - User login
- `GET /api/v1/users/me` - Get current user info
- `GET /api/v1/reports/` - Get reports
- `GET /api/v1/downloads/` - Get downloads

## Database

The application uses PostgreSQL. Make sure to update the `DATABASE_URL` in your `.env` file.
