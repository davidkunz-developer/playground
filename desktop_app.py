import webview
import threading
import os
import time

# Zde je URL tvého serveru na Renderu
SERVER_URL = "https://playground-kdui.onrender.com/"

def start_app():
    # Vytvoří okno, které se chová jako desktopová aplikace
    # Načte přímo tvůj frontend z Renderu
    webview.create_window('Robot Cockpit', SERVER_URL, width=1200, height=800)
    webview.start()

if __name__ == "__main__":
    start_app()
