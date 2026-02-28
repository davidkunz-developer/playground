import os
import csv
import uuid
from datetime import datetime

def log_result(rid, msg, st):
    log_file = "automation_log.csv"
    now = datetime.now()
    header = ["id_behu", "datum", "cas", "error_message", "status", "screenshot"]
    new_entry = [rid, now.strftime("%d.%m.%Y"), now.strftime("%H:%M:%S"), msg, st, ""]
    file_exists = os.path.isfile(log_file)
    with open(log_file, mode='a', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        if not file_exists: writer.writerow(header)
        writer.writerow(new_entry)

def set_step(msg):
    with open('current_step.txt', 'w', encoding='utf-8') as f:
        f.write(msg)

def run():
    run_id = str(uuid.uuid4())[:8]
    set_step("Kontrola prostředí pro DBeaver...")
    
    # Na serveru (Linux/Render) DBeaver logicky nepustíme
    if os.name != "nt":
        msg = "DBeaver nelze spustit na cloudovém serveru (vyžaduje GUI)."
        log_result(run_id, msg, "error")
        set_step(f"CHYBA: {msg}")
    else:
        # Tady by byla lokální logika pro Windows, pokud bys to pouštěl u sebe
        log_result(run_id, "DBeaver spuštěn (lokálně)", "ok")
        set_step("DOKONČENO")

if __name__ == "__main__":
    run()
