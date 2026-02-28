FROM python:3.11-slim

# Instalace nezbytných balíčků
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpangocairo-1.0-0 \
    --no-install-recommends

# Instalace Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/googlechrome-linux-keyring.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/googlechrome-linux-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Nastavení pracovního adresáře
WORKDIR /app

# Kopírování závislostí a instalace
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopírování zbytku aplikace
COPY . .

# Spuštění serveru - Render vyžaduje naslouchání na portu z proměnné $PORT
CMD uvicorn server:app --host 0.0.0.0 --port ${PORT:-8000}
