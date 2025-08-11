FROM python:3.11-slim

RUN apt-get update && apt-get install -y make && rm -rf /var/lib/apt/lists/*

ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"

RUN pip install poetry==1.7.1 --no-cache-dir

WORKDIR /app
COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --no-interaction --no-ansi

COPY . .

ENTRYPOINT ["/bin/bash", "-c", "poetry run make beat"]
