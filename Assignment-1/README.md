# Assignment 1 - Task API

This project is a simple REST API built with **FastAPI**. It provides CRUD operations for managing tasks and uses **PostgreSQL** as the database.

The application is containerized using **Docker** and **Docker Compose**, with separate containers for the FastAPI application and PostgreSQL database.

## Technologies

* Python 3.12
* FastAPI
* Uvicorn
* PostgreSQL
* Psycopg
* Pydantic
* Docker
* Docker Compose
* `uv` package manager

## Project Structure

```text
Assignment-1/
│
├── main.py
├── database.py
├── models.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pyproject.toml
├── uv.lock
├── .dockerignore
└── README.md
```

## Requirements

To run the project locally, you need:

* Python 3.12 or newer
* `uv`
* Docker Desktop

Docker Desktop is required if you want to run the application and PostgreSQL database using Docker Compose.

## Install `uv`

On Windows PowerShell:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

After installation, close and reopen your terminal, then check that `uv` is installed:

```powershell
uv --version
```

## Install Project Dependencies Locally

From the project folder:

```powershell
uv sync
```

This creates or updates the `.venv` virtual environment and installs the dependencies defined in `pyproject.toml` and `uv.lock`.

## Database

This project uses **PostgreSQL** instead of SQLite.

PostgreSQL runs inside a Docker container using the official PostgreSQL image.

The database configuration is defined in `docker-compose.yml`:

```yaml
db:
  image: postgres:latest
  environment:
    POSTGRES_PASSWORD: dev
    POSTGRES_DB: tasks
    POSTGRES_USER: postgres
  volumes:
    - taskdata:/var/lib/postgresql/data
```

The database is named:

```text
tasks
```

The PostgreSQL container is accessible from the FastAPI container using the hostname:

```text
db
```

The application uses the following database connection string:

```text
postgresql://postgres:dev@db:5432/tasks
```

The `db` hostname works because Docker Compose automatically creates a network for the services.

## Docker Compose

The project contains two services:

```text
FastAPI API
    |
    | PostgreSQL connection
    ↓
PostgreSQL Database
```

The services are:

| Service | Description         | Port   |
| ------- | ------------------- | ------ |
| `api`   | FastAPI application | `3000` |
| `db`    | PostgreSQL database | `5432` |

The PostgreSQL data is persisted using a Docker volume named:

```text
taskdata
```

This means database data is preserved even if the PostgreSQL container is removed.

## Run with Docker

Make sure **Docker Desktop is running**.

From the project directory:

```powershell
docker compose up --build
```

The `--build` option rebuilds the FastAPI Docker image when application or Docker configuration changes.

To run the containers in the background:

```powershell
docker compose up --build -d
```

Check the running containers:

```powershell
docker compose ps
```

View application logs:

```powershell
docker compose logs api
```

View PostgreSQL logs:

```powershell
docker compose logs db
```

Stop the containers:

```powershell
docker compose down
```

To stop the containers and also remove the PostgreSQL volume:

```powershell
docker compose down -v
```

> **Warning:** `docker compose down -v` deletes the `taskdata` volume and therefore removes the PostgreSQL database data.

## Run Without Docker

The project can also be run locally using the Python environment.

However, PostgreSQL must still be available locally or through another PostgreSQL server.

Set the `DATABASE_URL` environment variable to your PostgreSQL connection string.

For example:

```text
DATABASE_URL=postgresql://postgres:dev@localhost:5432/tasks
```

Then start FastAPI:

```powershell
uv run fastapi dev main.py
```

The API will run at:

```text
http://127.0.0.1:8000
```

When running through Docker Compose, the API uses port `3000`:

```text
http://localhost:3000
```

## API Documentation

When running with Docker:

```text
http://localhost:3000/docs
```

FastAPI also provides an alternative ReDoc interface:

```text
http://localhost:3000/redoc
```

When running locally with `uv`:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

| Method   | Endpoint      | Description       |
| -------- | ------------- | ----------------- |
| `GET`    | `/`           | API information   |
| `GET`    | `/health`     | Health check      |
| `GET`    | `/tasks`      | Get all tasks     |
| `GET`    | `/tasks/{id}` | Get a task by ID  |
| `POST`   | `/tasks`      | Create a new task |
| `PUT`    | `/tasks/{id}` | Update a task     |
| `DELETE` | `/tasks/{id}` | Delete a task     |

## Request Body

The `POST` and `PUT` endpoints use a JSON request body.

The task model is:

```json
{
  "title": "Learn FastAPI",
  "done": false
}
```

## Example Requests

### Get All Tasks

```powershell
curl http://localhost:3000/tasks
```

Example response:

```json
[
  {
    "id": 1,
    "title": "Learn PostgreSQL",
    "done": false
  },
  {
    "id": 2,
    "title": "Build a Todo API",
    "done": false
  },
  {
    "id": 3,
    "title": "Submit assignment",
    "done": true
  }
]
```

### Get a Task by ID

```powershell
curl http://localhost:3000/tasks/1
```

### Create a Task

```powershell
curl -X POST "http://localhost:3000/tasks" `
  -H "Content-Type: application/json" `
  -d '{"title":"Study FastAPI","done":false}'
```

### Update a Task

```powershell
curl -X PUT "http://localhost:3000/tasks/1" `
  -H "Content-Type: application/json" `
  -d '{"title":"Learn FastAPI and PostgreSQL","done":true}'
```

### Delete a Task

```powershell
curl -X DELETE http://localhost:3000/tasks/1
```

## Initial Database Data

When the application starts, it creates the `tasks` table if it does not already exist.

The table structure is:

```sql
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    done BOOLEAN NOT NULL
);
```

If the table is empty, the application inserts the following sample tasks:

```text
Learn PostgreSQL
Build a Todo API
Submit assignment
```

## SQL Query

One SQL query used by the API to retrieve all tasks is:

```sql
SELECT * FROM tasks;
```

A task can also be retrieved by its ID:

```sql
SELECT * FROM tasks WHERE id = %s;
```

## Database Persistence

PostgreSQL data is stored in the Docker volume:

```text
taskdata
```

The volume is mounted to:

```text
/var/lib/postgresql/data
```

Therefore, restarting the containers does not remove the database data.

To completely reset the database:

```powershell
docker compose down -v
docker compose up --build
```

## Environment Variables

The application uses the following environment variable:

```text
DATABASE_URL
```

When running inside Docker Compose:

```text
DATABASE_URL=postgresql://postgres:dev@db:5432/tasks
```

The `.env` file should not be committed to Git if it contains sensitive credentials.

## Dockerfile

The FastAPI application is built using Python 3.12:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 3000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]
```

## Docker Compose Configuration

The application and database are managed using Docker Compose.

```yaml
services:
  api:
    build: .
    ports:
      - "3000:3000"
    environment:
      DATABASE_URL: "postgresql://postgres:dev@db:5432/tasks"
    depends_on:
      - db

  db:
    image: postgres:latest
    environment:
      POSTGRES_PASSWORD: dev
      POSTGRES_DB: tasks
      POSTGRES_USER: postgres
    volumes:
      - taskdata:/var/lib/postgresql/data

volumes:
  taskdata:
```

## Health Check

The API provides a simple health-check endpoint:

```powershell
curl http://localhost:3000/health
```

Response:

```json
{
  "status": "ok"
}
```

## Notes

* PostgreSQL is used as the persistent database.
* Docker Compose manages both the API and PostgreSQL services.
* The FastAPI application communicates with PostgreSQL using Psycopg.
* The database is persisted through a Docker volume.
* FastAPI automatically provides interactive API documentation through Swagger UI.
* The API uses Pydantic models for request validation.
* The API is available on port `3000` when running through Docker Compose.
