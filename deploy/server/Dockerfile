FROM python:3.11-slim

RUN apt-get update && apt-get install -y make && rm -rf /var/lib/apt/lists/*

ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"

RUN pip install poetry==1.7.1 --no-cache-dir

WORKDIR /app
COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --no-interaction --no-ansi

COPY . .

ENTRYPOINT ["/bin/bash", "-c", "poetry run make certificates && poetry run make migration-upgrade && poetry run make seed && exec poetry run gunicorn server:server --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000"]
