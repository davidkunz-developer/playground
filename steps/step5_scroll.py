step_name = "scroll na sekci Kontakty"
error_message = "Sekce Kontakt nenalezena."

def run(browser, page):
    # Playwrightův nativní scroll
    kontakt = page.locator("#contact")
    # Tímto se zajistí, že je viditelný
    kontakt.scroll_into_view_if_needed()
    # Malá pauza pro oči (a stabilitu)
    page.wait_for_timeout(500)
    
    # Pojistíme to explicitním scrollem o kus dolů, je-li to hlouběji
    page.mouse.wheel(0, 200)
