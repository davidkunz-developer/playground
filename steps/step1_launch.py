from playwright.sync_api import sync_playwright

step_name = "spuštění prohlížeče"
error_message = "Nepodařilo se spustit motor Playwright."

def run():
    # Inicializace synchronního Playwrightu
    pw = sync_playwright().start()
    
    # Spustíme Chrome/Chromium v headless režimu pro Render
    # headless=True je výchozí, pro jistotu explicitně
    browser = pw.chromium.launch(headless=True)
    
    # Vytvoření kontextu s Full HD rozlišením
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    )
    
    # Nová stránka
    page = context.new_page()
    
    # Playwright má vestavěný timeout, nastavíme ho globálně na 10s
    page.set_default_timeout(10000)
    
    return browser, page, pw
