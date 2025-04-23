FROM python:3.12-slim

# Installe uv et uvicorn directement via pip
RUN pip install uv uvicorn

WORKDIR /app

COPY pyproject.toml uv.lock /app/

# Installe les dépendances à partir des fichiers
RUN uv pip install --system --no-deps .

# Copie le code de l'app
COPY ./app /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
