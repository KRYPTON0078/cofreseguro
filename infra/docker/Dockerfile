FROM python:3.11-slim
WORKDIR /app
COPY backend/pyproject.toml backend/README.md ./
COPY backend/src ./src
RUN pip install --no-cache-dir -e .
EXPOSE 8080
CMD ["uvicorn", "cofreseguro.main:app", "--host", "0.0.0.0", "--port", "8080"]
