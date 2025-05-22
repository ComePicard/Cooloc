# Cooloc

Self-hosted roommate and vacation spending manager

⚠️ Project is still in development, some feature may be not worked properly.

## Requirements
- Python 3.12 ([download](https://www.python.org/downloads/release/python-31210/))
- UV
- Docker

To initialize the project
```bash
git clone https://github.com/ComePicard/Cooloc.git
cd cooloc
uv pip install .
```
Run with `uv run-dev.py`

## Features
- Create groups (roommates & vacation)
- Manage documents
- Manage spending and dispatch them
- Manage your profile
- Invitation system

## Installation

### Docker

```bash
docker compose up -d
```

Backend: **http://localhost:8000**

Frontend: **http://localhost:8080**

### Command

Pylint execution

```bash
pylint app  
```

## Contributions

### Issues

If you had errors, you can help team by creating an issues, please share screen capture and console logs.

### Conventions

All pull requests must be prefixed with:
- feat()
- fix()
- ci()
- refactor()
