FROM python:3.10-slim

# Install system dependencies (FFmpeg is must)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install requirements first
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
# Yahan 'tgcalls' ko manually handle karne ki zaroorat nahi
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

CMD ["python3", "main.py"]
