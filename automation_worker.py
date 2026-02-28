import os
import csv
import sys
import uuid
import time
from datetime import datetime

# Importujeme ty naše nové "skládačky" ze složky steps
from steps import init_browser, nav_to_web, submit_form

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
    set_step("Startuji modulární motor (LEGO REŽIM)...")
    
    driver = None
    curr_step = None # Aktuálně běžící modul
    
    try:
        # KROK 1: Start prohlížeče
        curr_step = init_browser
        set_step("Nastavuji Full HD prohlížeč...")
        driver, wait = init_browser.run()

        # KROK 2: Web a Cookies
        curr_step = nav_to_web
        set_step("Navazuji spojení s webem a řeším cookies...")
        nav_to_web.run(driver, wait)

        # KROK 3: Formulář a Odeslání
        curr_step = submit_form
        set_step("Vyplňuji a odesílám formulář...")
        submit_form.run(driver, wait)
        
        # KROK 4: Screenshot (udělá orchestrátor pro jistotu)
        set_step("Vyřizuji důkaz (screenshot)...")
        ss_dir = "screenshots"
        if not os.path.exists(ss_dir): os.makedirs(ss_dir)
        ss_name = f"screenshot_{run_id}.png"
        ss_path = os.path.join(ss_dir, ss_name)
        driver.get_screenshot_as_file(ss_path)
        
        log_result(run_id, "", "ok", f"/screenshots/{ss_name}")
        set_step("DOKONČENO")
        
    except Exception as e:
        # Tady se děje ta magie s chybou z aktuálního kroku!
        # Pokud modul havaruje, vezmeme jeho specifickou error_message
        specific_error = getattr(curr_step, 'error_message', 'Neočekávaná chyba systému.')
        full_error = f"{specific_error} (Detaily: {str(e)})"
        
        log_result(run_id, full_error, "error")
        set_step(f"CHYBA: {full_error}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    run()
