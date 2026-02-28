FROM python:3.11-slim

# Instalace nezbytných systémových knihoven pro Playwright
# (Playwright install-deps to umí automaticky)
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
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Nastavení pracovního adresáře
WORKDIR /app

# Kopírování závislostí a instalace
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instalace Playwright Chromium a jeho systémových závislostí
RUN playwright install --with-deps chromium

# Kopírování zbytku aplikace
COPY . .

# Spuštění serveru
CMD uvicorn server:app --host 0.0.0.0 --port ${PORT:-8000}
