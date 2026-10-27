FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN python -m pip install --no-cache-dir --upgrade pip

COPY app.py .

RUN useradd --system --no-create-home appuser \
    && chown -R appuser:appuser /app

USER appuser

CMD ["python", "app.py"]
