import os
import csv
import sys
import uuid
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def log_result(rid, msg, st, ss=""):
    log_file = "automation_log.csv"
    now = datetime.now()
    header = ["id_behu", "datum", "cas", "error_message", "status", "screenshot"]
    new_entry = [rid, now.strftime("%d.%m.%Y"), now.strftime("%H:%M:%S"), msg, st, ss]
    file_exists = os.path.isfile(log_file)
    with open(log_file, mode='a', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        if not file_exists: writer.writerow(header)
        writer.writerow(new_entry)

def set_step(msg):
    with open('current_step.txt', 'w', encoding='utf-8') as f:
        f.write(msg)
    print(f"📍 {msg}")

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def run():
    run_id = str(uuid.uuid4())[:8]
    set_step("Startuji Turbo Engine...")
    
    # Nastavení driveru s cache (zrychlí start o cca 5-8 vteřin)
    os.environ['WDM_LOG_LEVEL'] = '0'
    os.environ['WDM_LOCAL_PATH'] = os.path.join(os.getcwd(), ".wdm")

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--window-size=1280,720")
    
    # Úspora RAM (bez obrázků)
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)

    driver = None
    try:
        set_step("Otevírám prohlížeč...")
        # ChromeDriver s minimálním zpožděním při startu
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        wait = WebDriverWait(driver, 15) # Max 15s čekání, ale skončí hned jak najde prvek

        set_step("Naviguji na web...")
        driver.get("https://www.david-kunz-automation.com")

        # --- COOKIES ---
        try:
            set_step("Potvrzuji cookies...")
            # Hledáme tlačítko 'Rozumím' nebo 'Accept'
            cookie_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Rozumím') or contains(text(), 'Accept')]")))
            cookie_btn.click()
            time.sleep(0.5) # Krátká pauza na zmizení lišty
        except:
            print("Cookie lišta nenalezena.")

        set_step("Hledám sekci Kontakt...")
        # Místo time.sleep(2) čekáme na prvek
        contact_section = wait.until(EC.presence_of_element_located((By.ID, "contact-section")))
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});", contact_section)
        
        set_step("Vyplňuji formulář...")
        # Čekáme na první pole, abychom měli jistotu
        first_name_field = wait.until(EC.element_to_be_clickable((By.ID, "firstName")))
        
        # Super rychlé psaní
        first_name_field.send_keys("Robot")
        driver.find_element(By.ID, "lastName").send_keys("Tonda")
        driver.find_element(By.ID, "email").send_keys("tonda.robot@solutions.cz")
        driver.find_element(By.ID, "message").send_keys("Tato zpráva byla odeslána automaticky robotem v ostrém Turbo režimu.")
        
        set_step("Odesílám formulář...")
        submit_btn = driver.find_element(By.CSS_SELECTOR, "#contact-form button[type='submit']")
        driver.execute_script("arguments[0].click();", submit_btn) # Jistější odeslání přes JS
        
        # Počkáme na potvrzení (třeba chvilku)
        time.sleep(1)

        set_step("Pořizuji screenshot...")
        ss_dir = "screenshots"
        if not os.path.exists(ss_dir): os.makedirs(ss_dir)
        ss_name = f"screenshot_{run_id}.png"
        ss_path = os.path.join(ss_dir, ss_name)
        driver.get_screenshot_as_file(ss_path) # Rychlejší metoda
        
        log_result(run_id, "", "ok", f"/screenshots/{ss_name}")
        set_step("DOKONČENO")
        
    except Exception as e:
        error_msg = str(e)
        log_result(run_id, error_msg, "error")
        set_step(f"CHYBA: {error_msg}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    run()
