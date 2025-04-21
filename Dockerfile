FROM python:3.11-slim

WORKDIR /app

COPY requirements__.txt .
RUN pip install --no-cache-dir -r requirements__.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]