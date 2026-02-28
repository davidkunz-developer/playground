step_name = "maximalizování"
error_message = "Chyba při nastavování rozlišení."

def run(browser, page):
    # Desktop Full HD (již podchyceno v contextu, ale pro formu)
    page.set_viewport_size({"width": 1920, "height": 1080})
