FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libdbus-1-3 \
    libx11-6 \
    libx11-xcb1 \
    libxkbcommon0 \
    libxkbcommon-x11-0 \
    libxext6 \
    libxrender1 \
    libxi6 \
    libxfixes3 \
    libfontconfig1 \
    libfreetype6 \
    libxcb1 \
    libxcb-cursor0 \
    libxcb-xinerama0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-m", "arc"]
