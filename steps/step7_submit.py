step_name = "Odeslat"
error_message = "Chyba při odesílání nebo čekání na 'ODESLÁNO'."

def run(browser, page):
    # Odeslání formuláře
    submit_btn = page.locator("#contact-form button[type='submit']")
    submit_btn.click()
    
    # Čekáme, až se v elementu #form-status objeví text "ODESLÁNO"
    # Playwrightův selector pohlídá i textový obsah
    page.wait_for_selector("#form-status:has-text('ODESLÁNO')", timeout=10000)
    
    # Krátký dozvuk
    page.wait_for_timeout(500)
