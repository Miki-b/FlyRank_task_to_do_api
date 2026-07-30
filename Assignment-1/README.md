# Assignment 1 - Task API

This project is a simple REST API built with FastAPI. It manages tasks in a SQLite database and supports creating, reading, updating, and deleting tasks.

## Requirements

- Python 3.14 or newer
- `uv` package manager

## Install `uv`

On Windows PowerShell:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

After installation, close and reopen your terminal, then check that `uv` is installed:

```powershell
uv --version
```

## Install Project Dependencies

From the project folder:

```powershell
cd "c:\Users\Dell\OneDrive\Documenti\Self-development\FlyRank Internship\Assignment-1"
uv sync
```

This creates or updates the `.venv` virtual environment and installs the dependencies from `pyproject.toml` and `uv.lock`.

## Run the Project

Start the FastAPI development server with this command:

```powershell
uv run fastapi dev main.py
```

The API will run at:

```text
http://127.0.0.1:8000
```

Interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## Database

This project uses SQLite because it is simple for a small assignment API: the whole database is stored in a single file, it requires zero database server setup, and the data survives app restarts.

The database file is named `tasks.db`. It is created automatically in the project folder when `main.py` runs:

```text
Assignment-1/tasks.db
```

This file is usually added to `.gitignore` so each cloned copy of the project starts with a fresh local database.

## DB Browser Screenshot

Screenshot of `tasks.db` opened in DB Browser for SQLite:

![tasks.db open in DB Browser for SQLite](docs/db-browser-tasks.png)

## Stage 4 SQL Query

One SQL query run in Stage 4 was:

```sql
SELECT * FROM tasks;
```

## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/` | API information |
| `GET` | `/health` | Health check |
| `GET` | `/tasks` | Get all tasks |
| `GET` | `/tasks/{id}` | Get a task by ID |
| `POST` | `/tasks?title=New Task` | Create a new task |
| `PUT` | `/tasks/{id}?title=Updated Task&done=true` | Update a task |
| `DELETE` | `/tasks/{id}` | Delete a task |

## Example Requests

Get all tasks:

```powershell
curl http://127.0.0.1:8000/tasks
```

Create a task:

```powershell
curl -X POST "http://127.0.0.1:8000/tasks?title=Study FastAPI"
```

Update a task:

```powershell
curl -X PUT "http://127.0.0.1:8000/tasks/1?title=Wake up&done=true"
```

Delete a task:

```powershell
curl -X DELETE http://127.0.0.1:8000/tasks/1
```
