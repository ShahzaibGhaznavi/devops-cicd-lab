FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN python -m pip install --no-cache-dir --upgrade pip==26.2.2

COPY app.py .

RUN adduser -D -H appuser \
    && chown -R appuser:appuser /app

USER appuser

CMD ["python", "app.py"]
