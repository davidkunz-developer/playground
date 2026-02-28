import webview
import threading
import os
import time

# Zde bude URL tvého serveru na Renderu (poté co ho nasadíš)
# Pro testování teď nechávám localhost
SERVER_URL = "http://127.0.0.1:8000"

def start_app():
    # Vytvoří okno, které se chová jako desktopová aplikace
    webview.create_window('Robot Cockpit', SERVER_URL, width=1200, height=800)
    webview.start()

if __name__ == "__main__":
    start_app()
