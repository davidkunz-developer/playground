from fastapi import FastAPI, BackgroundTasks, Header, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import papermill as pm
import pandas as pd
import os
import uvicorn
import json
import time

app = FastAPI()

# --- KONFIGURACE ZABEZPEČENÍ ---
# Na Renderu si toto nastavíš v 'Environment Variables'
API_KEY = os.environ.get("ROBOT_API_KEY", "moje-tajne-heslo-123")
LOG_FILE = "automation_log.csv"

def verify_api_key(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Neautorizovaný přístup. Špatný API klíč.")
    return x_api_key

NOTEBOOKS = {
    "dbeaver": "dbeaver_launcher.ipynb",
    "playground": "automation_playground.ipynb"
}
SCREENSHOT_DIR = "screenshots"

if not os.path.exists(SCREENSHOT_DIR):
    os.makedirs(SCREENSHOT_DIR)

app.mount(f"/{SCREENSHOT_DIR}", StaticFiles(directory=SCREENSHOT_DIR), name=SCREENSHOT_DIR)

@app.get("/")
async def get_index():
    # Používáme main_v2.html pro vynucení aktualizace frontendu u uživatele
    return FileResponse("main_v2.html")

@app.get("/logs")
async def get_logs(api_key: str = Depends(verify_api_key)):
    if not os.path.exists(LOG_FILE):
        return JSONResponse(content=[])
    try:
        df = pd.read_csv(LOG_FILE, encoding='utf-8-sig')
        df = df.fillna("")
        logs = df.to_dict(orient="records")
        return JSONResponse(content=logs[::-1])
    except Exception as e:
        print(f"Chyba při čtení logů: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/status")
async def get_status(api_key: str = Depends(verify_api_key)):
    if not os.path.exists("current_step.txt"):
        return JSONResponse(content={"step": "Systém připraven"})
    try:
        with open("current_step.txt", "r", encoding="utf-8") as f:
            return JSONResponse(content={"step": f.read()})
    except:
        return JSONResponse(content={"step": "Pracuji..."})

def execute_worker_task():
    # Agresivně vyčistíme RAM a spustíme lehký skript
    if os.name != "nt": 
        # Vyčistíme staré procesy
        os.system("pkill -f chrome || true")
        os.system("pkill -f chromedriver || true")
    
    # Spustíme lehký Python worker místo těžkého notebooku
    # To ušetří cca 150-200 MB RAM (nebudeme muset mít Jupyter Kernel)
    try:
        os.system(f"python automation_worker.py")
    except Exception as e:
        with open("current_step.txt", "w", encoding="utf-8") as f: 
            f.write(f"CHYBA: {str(e)}")

@app.post("/run/{notebook_id}")
async def run_automation(notebook_id: str, background_tasks: BackgroundTasks, api_key: str = Depends(verify_api_key)):
    # Inicializace statusu pro uživatele
    with open("current_step.txt", "w", encoding="utf-8") as f: 
        f.write("Zahajuji odlehčenou misi...")
    
    # Spustíme úlohu na pozadí (lehký worker)
    background_tasks.add_task(execute_worker_task)
    
    return {"status": "success", "message": "Robot byl vypuštěn (odlehčená verze)."}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
