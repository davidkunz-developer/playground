step_name = "cookies (pokud jsou)"
error_message = "Chyba při zpracování cookie banneru."

def run(browser, page):
    # Selector pro běžné cookie buttony
    # Playwrightův selector podporuje 'has-text' což je super rychlé
    banner = page.locator("//button[contains(text(), 'SOUHLASÍM') or contains(text(), 'Rozumím') or contains(text(), 'Accept')]")
    
    # Krátký timeout pro kontrolu přítomnosti - 3 sekundy stačí
    if banner.is_visible(timeout=3000):
        banner.click()
        # Malá pauza pro zmizení banneru
        page.wait_for_timeout(500)
    else:
        # Pokud není, nic se neděje
        pass
