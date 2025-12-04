FROM python:3.11-slim

# Set workdir
WORKDIR /app

# Install OS dependencies (postgres, etc)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Folder untuk logs
RUN mkdir -p logs

# Collect static (kalau ada)
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

CMD ["sh", "-c", "gunicorn mental_health_chatbot.wsgi:application --bind 0.0.0.0:${PORT:-8080}"]


