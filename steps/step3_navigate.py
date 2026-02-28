step_name = "vepsání url"
error_message = "Cíl nenalezen nebo timeout při načítání."

def run(browser, page):
    # Otevření stránky s timeoutem 10s (již nastaven globálně v S1)
    page.goto("https://www.david-kunz-automation.com", wait_until="domcontentloaded")
