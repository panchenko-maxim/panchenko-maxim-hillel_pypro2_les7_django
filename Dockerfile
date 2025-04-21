FROM python:3.11-slim

RUN pip install --upgrade pip && apt-get update && apt-get install -y libpq-dev && rm -rf /var/lib/apt/list/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./task_manager /app

EXPOSE 8000