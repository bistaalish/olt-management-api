FROM python:3.8-slim

# Install build dependencies for cryptography
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
 && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run uvicorn with logging to applog.txt
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --reload >> logs/applog.txt 2>&1"]
