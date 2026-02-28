import os
import csv
import uuid
import time
from datetime import datetime

# Import rozdělených kroků
from steps import step1_launch, step2_maximize, step3_navigate, step4_cookies, step5_scroll, step6_fill, step7_submit

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
    print(f"STAV: {msg}")

def run():
    run_id = str(uuid.uuid4())[:8]
    set_step("Zahajuji proces")
    
    driver = None
    curr_mod = None
    
    # Seznam kroků k provedení
    process_flow = [
        step1_launch,
        step2_maximize,
        step3_navigate,
        step4_cookies,
        step5_scroll,
        step6_fill,
        step7_submit
    ]
    
    try:
        # Postupné spouštění skriptů
        for module in process_flow:
            curr_mod = module
            set_step(module.step_name)
            
            if module == step1_launch:
                driver, wait = module.run()
            else:
                module.run(driver, wait)

        # Finální screenshot
        set_step("Ukládám potvrzení")
        ss_dir = "screenshots"
        if not os.path.exists(ss_dir): os.makedirs(ss_dir)
        ss_name = f"screenshot_{run_id}.png"
        ss_path = os.path.join(ss_dir, ss_name)
        driver.get_screenshot_as_file(ss_path)
        
        log_result(run_id, "", "ok", f"/screenshots/{ss_name}")
        set_step("DOKONČENO")
        
    except Exception as e:
        error_prefix = getattr(curr_mod, 'error_message', 'Neidentifikovaná chyba')
        full_error = f"{error_prefix} ({str(e)})"
        log_result(run_id, full_error, "error")
        set_step(f"CHYBA: {full_error}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    run()
