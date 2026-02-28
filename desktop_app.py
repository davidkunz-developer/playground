import webview
import threading
import os
import time

# Zde je URL tvého serveru na Renderu
SERVER_URL = "https://playground-1-tgou.onrender.com"

def start_app():
    # Přidáme časové razítko k URL, aby se vynutilo načtení nejnovější verze (bypass cache)
    unique_url = f"{SERVER_URL}?v={int(time.time())}"
    webview.create_window('AI Robo Cockpit', unique_url, width=1200, height=800)
    webview.start()

if __name__ == "__main__":
    start_app()
