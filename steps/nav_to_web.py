import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# Definice kroku a chyby
step_name = "Naviguji na web a řeším cookies"
error_message = "Chyba při navigaci na web nebo odklikávání cookies."

def run(driver, wait):
    driver.get("https://www.david-kunz-automation.com")
    
    # --- VĚTVENÍ: COOKIE LIŠTA ---
    try:
        # Použijeme krátký timeout (3s), abychom nezdržovali, pokud tam cookies nejsou
        from selenium.webdriver.support.ui import WebDriverWait
        cookie_wait = WebDriverWait(driver, 3) 
        
        # Hledáme tlačítko 'SOUHLASÍM'
        cookie_btn = cookie_wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'SOUHLASÍM') or contains(., 'Rozumím') or contains(., 'Accept')]")))
        
        print("📍 VĚTEV A: Cookies nalezeny, potvrzuji...")
        driver.execute_script("arguments[0].click();", cookie_btn)
        time.sleep(1) 
    except:
        # Tady je ta druhá větev - neděláme nic a pokračujeme
        print("📍 VĚTEV B: Cookies nenalezeny, pokračuji v misi...")

    # Najdeme sekci kontakt (to už je společná cesta)
    contact_section = wait.until(EC.presence_of_element_located((By.ID, "contact-section")))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});", contact_section)
