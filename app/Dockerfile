FROM python:3.9-slim
WORKDIR .
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py
HEALTHCHECK --interval=30s --timeout=3s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "3", "app:app"]
