# Task API

A RESTful CRUD API for managing tasks. It is built with FastAPI, stores data in PostgreSQL, and can be run as a two-container application with Docker Compose.

## Features

- Create tasks
- List all tasks
- Get one task by ID
- Replace a task's title and completion status
- Delete tasks
- Create the `tasks` table automatically when the API starts
- Check the active database connection
- Explore the API through FastAPI's interactive documentation

## Tech stack

- Python 3.11
- FastAPI
- Pydantic
- Uvicorn
- PostgreSQL
- Psycopg 3
- Docker and Docker Compose

## Project structure

```text
.
├── compose.yaml       # Docker Compose services for the API and PostgreSQL
├── database.py        # Database connection helper
├── Dockerfile         # API container image
├── mainfile.py        # FastAPI application and routes
├── requirements.txt   # Python dependencies
└── README.md
```

## Database schema

The application creates this table on startup if it does not already exist:

```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    done BOOLEAN DEFAULT FALSE
);
```

## Run with Docker Compose

### Prerequisites

- Docker Desktop (or Docker Engine with Docker Compose)

### Start the application

```bash
git clone https://github.com/mtalha909/CRUD_Backend.git
cd CRUD_Backend
docker compose up --build
```

The API is available at `http://localhost:8000`.

Docker Compose starts:

- `api` — the FastAPI application, exposed on port `8000`
- `db` — PostgreSQL 18, exposed on port `5432`

The PostgreSQL data is stored in the named Docker volume `taskdata`, so it remains available after containers are stopped.

### Stop the application

```bash
docker compose down
```

To also remove the stored PostgreSQL data:

```bash
docker compose down -v
```

## Run locally without Docker

### Prerequisites

- Python 3.11 or later
- A running PostgreSQL server

### Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root and set `DATABASE_URL` to your PostgreSQL connection string:

```env
DATABASE_URL=postgresql://postgres:dev@localhost:5432/tasks
```

Start the API:

```bash
uvicorn mainfile:app --reload
```

The application creates the `tasks` table when it starts. The database named in `DATABASE_URL` must already exist.

## API documentation

Once the server is running, open:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/test-db` | Returns the connected database name, or an error message if the connection fails. |
| `GET` | `/tasks` | Returns all tasks ordered by ID. |
| `GET` | `/tasks/{task_id}` | Returns one task. Responds with `404` if it does not exist. |
| `POST` | `/tasks` | Creates a task. |
| `PUT` | `/tasks/{task_id}` | Replaces a task's title and `done` value. Responds with `404` if it does not exist. |
| `DELETE` | `/tasks/{task_id}` | Deletes a task. Responds with `404` if it does not exist. |

### Task request body

`POST /tasks` and `PUT /tasks/{task_id}` accept:

```json
{
  "title": "Finish the assignment",
  "done": false
}
```

- `title` is required.
- `done` is optional and defaults to `false` when creating a task.

### Examples

Create a task:

```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"Finish the assignment\",\"done\":false}"
```

Get all tasks:

```bash
curl http://localhost:8000/tasks
```

Update task `1`:

```bash
curl -X PUT http://localhost:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"Finish the assignment\",\"done\":true}"
```

Delete task `1`:

```bash
curl -X DELETE http://localhost:8000/tasks/1
```

## Configuration used by Docker Compose

The Compose configuration supplies this connection URL to the API container:

```env
DATABASE_URL=postgresql://postgres:dev@db:5432/tasks
```

The PostgreSQL service is configured with:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=dev
POSTGRES_DB=tasks
```

For a production deployment, replace these development credentials with secure values.
