step_name = "maximalizování"
error_message = "Nepodařilo se maximalizovat okno prohlížeče."

def run(driver, wait):
    driver.maximize_window()
    # V headless režimu občas maximize nefunguje 100%, tak pojistíme rozlišením
    driver.set_window_size(1920, 1080)
