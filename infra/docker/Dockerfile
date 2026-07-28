FROM python:3.11-slim AS builder
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*
COPY backend/pyproject.toml backend/README.md ./
COPY backend/src ./src
COPY policies ./policies
COPY datasets ./datasets
COPY backend/models ./models
RUN pip install --no-cache-dir -e ".[ocr]"

FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends tesseract-ocr tesseract-ocr-por \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -m -u 10001 cofre
COPY --from=builder /usr/local /usr/local
COPY --from=builder /app /app
COPY policies ./policies
COPY datasets ./datasets
COPY backend/models ./models
COPY docs/tips ./docs/tips
USER cofre
EXPOSE 8080
HEALTHCHECK CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/health')" || exit 1
CMD ["uvicorn", "cofreseguro.main:app", "--host", "0.0.0.0", "--port", "8080"]
