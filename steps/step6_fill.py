step_name = "Vyplnění formuláře"
error_message = "Chyba při vyplňování údajů do formuláře."

def run(browser, page):
    # Playwright's fill je mnohem spolehlivější
    page.fill("#firstName", "Robot")
    page.fill("#lastName", "Tonda")
    page.fill("#email", "tonda.robot@solutions.cz")
    page.fill("#phone", "+420 777 121 456")
    message_text = "Automatický test - Playwright Speed Edition (7 diskrétních kroků)."
    page.fill("#message", message_text)
