FROM python:3.10-slim

WORKDIR /app
COPY pyproject.toml poetry.lock ./

# Install Poetry and dependencies
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --only main --no-root

COPY . .

ENTRYPOINT ["python", "main.py"]