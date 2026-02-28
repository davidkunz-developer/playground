import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

step_name = "cookies"
error_message = "Chyba při zpracování cookie lišty."

def run(driver, wait):
    try:
        # Čekání na cookies (10 sekund dle požadavku)
        cookie_wait = WebDriverWait(driver, 10)
        cookie_btn = cookie_wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'SOUHLASÍM') or contains(., 'Rozumím') or contains(., 'Accept')]")))
        driver.execute_script("arguments[0].click();", cookie_btn)
        time.sleep(1)
        print("Cookies potvrzeny.")
    except:
        print("Cookies nenalezeny - přeskakuji.")
