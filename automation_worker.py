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

def run():
    run_id = str(uuid.uuid4())[:8]
    set_step("Startuji lehký engine...")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--single-process") # Nutné pro 512MB RAM
    
    if os.path.exists("/usr/bin/google-chrome"):
        chrome_options.binary_location = "/usr/bin/google-chrome"

    driver = None
    try:
        set_step("Otevírám prohlížeč...")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        
        set_step("Naviguji na web...")
        driver.get("https://www.david-kunz-automation.com")
        time.sleep(2)

        set_step("Hledám sekci Kontakt...")
        contact_section = driver.find_element(By.ID, "contact-section")
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});", contact_section)
        
        set_step("Vyplňuji formulář...")
        driver.find_element(By.ID, "firstName").send_keys("Robot")
        driver.find_element(By.ID, "lastName").send_keys("Tonda")
        driver.find_element(By.ID, "email").send_keys("tonda.robot@solutions.cz")
        driver.find_element(By.ID, "message").send_keys("Běh z lehkého Python workeru pro úsporu RAM.")
        
        set_step("Odesílám (simulace)...")
        # Zde by byl click, pro test jen simulujeme
        time.sleep(1)

        set_step("Pořizuji screenshot...")
        ss_dir = "screenshots"
        if not os.path.exists(ss_dir): os.makedirs(ss_dir)
        ss_name = f"screenshot_{run_id}.png"
        ss_path = os.path.join(ss_dir, ss_name)
        driver.save_screenshot(ss_path)
        
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
