# Lifting Website

Full-stack lifting tracker — FastAPI backend + Vite frontend.

## Quick Start

```bash
docker-compose up --build
```

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API docs (Swagger): http://localhost:8000/docs

## Common Commands

| Command | Description |
|---|---|
| `docker-compose up --build` | Build images and start all services |
| `docker-compose up` | Start services (no rebuild) |
| `docker-compose down` | Stop and remove containers |
| `docker-compose logs -f` | Tail logs from all services |
| `docker-compose logs -f backend` | Tail backend logs only |
| `docker-compose exec backend bash` | Shell into the backend container |
| `docker-compose exec frontend sh` | Shell into the frontend container |

## Local Development (without Docker)

```bash
# Backend — from the project root
fastapi run backend/app.py

# Frontend — from the frontend/ directory
npx vite --host
```

## Services

### Backend (FastAPI)
- Port: `8000`
- Runs with `--reload` for live code reloading
- Database: SQLite at `backend/data/database.db`
- Set `DATABASE_URL` env var to override the database path

### Frontend (Vite)
- Port: `5173`
- Hot-reload enabled via Vite dev server
- Set `VITE_API_URL` env var to control the backend URL (default: `http://localhost:8000`)
