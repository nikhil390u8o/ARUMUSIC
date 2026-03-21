FROM python:3.10-slim

# System dependencies for FFmpeg and builds
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Upgrade pip first
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Sabhi libraries ko manual install karo (No requirements.txt needed)
RUN pip install --no-cache-dir pyrogram pytgcalls[ffmpeg] yt-dlp youtube-search-python beautifulsoup4 aiohttp

# Baaki code copy karo
COPY . .

CMD ["python3", "main.py"]
