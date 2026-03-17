FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libgl1 \
    libxkbcommon-x11-0 \
    libxcb-xinerama0 \
    libxcb-cursor0 \
    libx11-xcb1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "beta.py"]