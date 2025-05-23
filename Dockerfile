FROM python:3.12-slim

RUN pip install uv uvicorn

WORKDIR /app

COPY pyproject.toml /app/

RUN pip install .

COPY ./app /app

EXPOSE 8000

CMD ["uvicorn", "run-dev.py", "--host", "0.0.0.0", "--port", "8000"]
