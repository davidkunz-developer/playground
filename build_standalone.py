import webview
import os
import sys

def get_resource_path(relative_path):
    """ Získá cestu k souboru (funguje pro vývoj i pro PyInstaller) """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def launch():
    # Teď načítáme LOKÁLNÍ soubor desktop_index.html, který bude uvnitř EXE
    html_file = get_resource_path("desktop_index.html")
    
    if not os.path.exists(html_file):
        # Pojistka pro případ, že by soubor chyběl
        print(f"ERROR: Soubor {html_file} nebyl nalezen!")
        return

    window = webview.create_window(
        'AI ROBO COCKPIT v3.0 (Offline FE)', 
        html_file, 
        width=1200, 
        height=850,
        resizable=True
    )
    
    # Spuštění s vyčištěnou cache
    webview.start(private_mode=True)

if __name__ == "__main__":
    launch()
