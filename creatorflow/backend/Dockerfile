FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ffmpeg \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV PORT=8000
EXPOSE 8000

# Default command runs the API via Gunicorn; WORKER_PROCESS=true switches to RQ worker
CMD ["/bin/bash", "-lc", "if [ \"$WORKER_PROCESS\" = \"true\" ]; then rq worker --url $REDIS_URL creatorflow-queue; else gunicorn wsgi:app -w 4 -k gthread -b 0.0.0.0:$PORT --timeout 120; fi"]