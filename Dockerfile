FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app/files

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

