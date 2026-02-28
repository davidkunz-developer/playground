import os
import csv
import uuid
import time
from datetime import datetime

# Import rozdělených kroků
from steps import step1_launch, step2_maximize, step3_navigate, step4_cookies, step5_scroll, step6_fill, step7_submit

def set_step(text):
    """Pomocná funkce pro zápis aktuálního stavu do souboru."""
    try:
        with open("current_step.txt", "w", encoding="utf-8") as f:
            f.write(text)
    except:
        pass

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

def take_screenshot(page, run_id):
    try:
        ss_dir = "screenshots"
        if not os.path.exists(ss_dir): os.makedirs(ss_dir)
        ss_name = f"screenshot_{run_id}.png"
        ss_path = os.path.join(ss_dir, ss_name)
        # Playwright screenshot
        page.screenshot(path=ss_path, full_page=False)
        return f"/screenshots/{ss_name}"
    except Exception as e:
        print(f"Screenshot s chybou: {e}")
        return ""

def run():
    run_id = str(uuid.uuid4())[:8]
    set_step("Zahajuji proces")
    
    browser = None
    page = None
    pw = None
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
        total_steps = len(process_flow)
        for i, module in enumerate(process_flow):
            curr_mod = module
            set_step(f"{module.step_name}|{i+1}|{total_steps}")
            
            if module == step1_launch:
                browser, page, pw = module.run()
            else:
                module.run(browser, page)
            
            # Krátká pauza pro UI refresh - s Playwrightem stačí míň
            time.sleep(0.3)

        # Finální screenshot
        set_step("Ukládám potvrzení")
        ss_url = take_screenshot(page, run_id)
        
        log_result(run_id, "Úspěšná mise!", "ok", ss_url)
        set_step("DOKONČENO")
        
    except Exception as e:
        # Pobereme jen čistou hlášku, žádné monster stacktracy
        clean_error = getattr(curr_mod, 'error_message', f"Chyba systému: {str(e)}")
        
        # Zkusíme udělat screenshot i při chybě
        ss_url = ""
        if page:
            ss_url = take_screenshot(page, run_id)
        
        log_result(run_id, clean_error, "error", ss_url)
        set_step("FAILED")
        print(f"Běloruská chyba: {e}") # Pro logy na Renderu
        
    finally:
        if browser:
            browser.close()
        if pw:
            pw.stop()

if __name__ == "__main__":
    run()
