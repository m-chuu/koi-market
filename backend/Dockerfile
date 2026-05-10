FROM python:3.12-slim

WORKDIR /app

# Install system dependencies for PostgreSQL and Cloud SQL Auth Proxy
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Cloud Run uses PORT environment variable
ENV PORT=8080

# Expose port (Cloud Run expects 8080 by default)
EXPOSE 8080

# Run with production settings
# Cloud Run injects PORT env var, uvicorn reads from $PORT
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}"]
