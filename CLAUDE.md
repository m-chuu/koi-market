# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Koi Market is an e-commerce application for selling Japanese koi fish. It uses a React frontend with a FastAPI backend, connected to a PostgreSQL database.

## Development Commands

### Frontend (from `frontend/` directory)
```bash
npm run dev      # Start Vite dev server (http://localhost:5173)
npm run build    # Production build
npm run lint     # Run ESLint
npm run preview  # Preview production build
```

### Backend (from `backend/` directory)
```bash
# Activate virtual environment first
source venv/bin/activate

# Run FastAPI server
uvicorn app.main:app --reload    # Starts on http://127.0.0.1:8000

# Seed the database
python seed.py
```

### Database
```bash
# Start PostgreSQL via Docker
docker-compose up -d

# Connection: postgresql://koi_user:koi_password@localhost:5432/koi_market_db
```

## Architecture

### Backend (`backend/app/`)
- **main.py**: FastAPI app entry point with CORS middleware configuration
- **database.py**: SQLAlchemy engine, session management, and `get_db` dependency
- **models.py**: SQLAlchemy ORM models (currently `Koi` model)
- **schemas.py**: Pydantic schemas for request/response validation (`KoiBase`, `KoiCreate`, `Koi`)
- **routers/**: API route modules (e.g., `kois.py` for `/kois` endpoints)

Database tables are auto-created on startup via `Base.metadata.create_all()`.

### Frontend (`frontend/src/`)
- **main.jsx**: React entry point
- **App.jsx**: Main component with koi product grid and cart state
- Uses Tailwind CSS for styling
- Currently uses mock data; API integration with axios is available

### API Endpoints
- `GET /` - API welcome message
- `GET /kois` - List all koi fish
- `POST /kois` - Create new koi fish

CORS is configured to allow requests from `localhost:5173` and `localhost:3000`.

## Configuration

- Backend environment variables: `backend/.env` (DATABASE_URL)
- Frontend dev server runs on port 5173 by default
- Backend accepts requests from frontend origins via CORS middleware
