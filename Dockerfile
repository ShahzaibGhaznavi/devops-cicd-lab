
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Apply available Debian security and package updates.
RUN apt-get update \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/*

COPY app.py .

RUN useradd --system --no-create-home appuser \
    && chown -R appuser:appuser /app

USER appuser

CMD ["python", "app.py"]
