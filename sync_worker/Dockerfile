FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# копируем код
COPY counters_api ./counters_api
COPY sync_worker ./sync_worker

# по умолчанию — периодический воркер
CMD ["python", "-m", "sync_worker.sync_app"]