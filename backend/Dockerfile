# Simple production-ready image
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENV PYTHONUNBUFFERED=1

# gunicorn by default; fall back to flask for local experiments
CMD ["gunicorn", "-c", "gunicorn.conf.py", "app:app"]
