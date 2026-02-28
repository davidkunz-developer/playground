import webview
import threading
import os
import time

# Zde je URL tvého serveru na Renderu
SERVER_URL = "https://playground-1-tgou.onrender.com"

import sys

def start_app():
    # Cesta pro PyInstaller (včetně přibalených souborů)
    if hasattr(sys, '_MEIPASS'):
        current_dir = sys._MEIPASS
    else:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
    html_file = os.path.join(current_dir, 'desktop_index.html')
    
    # Vytvoří okno, které načte lokální vzhled, ale data tahá z Renderu
    webview.create_window('AI Robo Cockpit', html_file, width=1200, height=800)
    webview.start()

if __name__ == "__main__":
    start_app()
