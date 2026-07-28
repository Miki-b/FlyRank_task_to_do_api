# Assignment 1 - Task API

This project is a simple REST API built with FastAPI. It manages an in-memory list of tasks and supports creating, reading, updating, and deleting tasks.

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

Start the FastAPI development server:

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
