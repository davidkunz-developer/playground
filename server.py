from fastapi import FastAPI, BackgroundTasks, Header, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
# import papermill as pm (odstraněno pro úsporu RAM)
import pandas as pd
import os
import uvicorn
import json
import time

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# --- CORS KONFIGURACE ---
# Musíme povolit přístup z jiných domén (např. z tvé lokální aplikace na ploše)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- KONFIGURACE ZABEZPEČENÍ ---
# Na Renderu si toto nastavíš v 'Environment Variables'
API_KEY = os.environ.get("ROBOT_API_KEY", "moje-tajne-heslo-123")
LOG_FILE = "automation_log.csv"

def verify_api_key(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Neautorizovaný přístup. Špatný API klíč.")
    return x_api_key

# NOTEBOOKS mapping odstraněn
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

def execute_worker_task(script_name: str):
    # Agresivně vyčistíme RAM a spustíme lehký skript
    if os.name != "nt": 
        os.system("pkill -f chrome || true")
        os.system("pkill -f chromedriver || true")
    
    try:
        # Spustíme konkrétní Python skript podle požadavku
        os.system(f"python {script_name}")
    except Exception as e:
        with open("current_step.txt", "w", encoding="utf-8") as f: 
            f.write(f"CHYBA: {str(e)}")

@app.post("/run/{action_id}")
async def run_automation(action_id: str, background_tasks: BackgroundTasks, api_key: str = Depends(verify_api_key)):
    # Inicializace statusu pro uživatele
    with open("current_step.txt", "w", encoding="utf-8") as f: 
        f.write("Zahajuji odlehčenou misi...")
    
    # Mapování akcí na čisté Python skripty
    script_map = {
        "automation_playground": "automation_worker.py",
        "playground": "automation_worker.py",
        "dbeaver_launcher": "dbeaver_worker.py",
        "dbeaver": "dbeaver_worker.py"
    }

    target_script = script_map.get(action_id, "automation_worker.py")
    
    # Spustíme úlohu na pozadí (lehký worker)
    background_tasks.add_task(execute_worker_task, target_script)
    
    return {"status": "success", "message": f"Mise '{action_id}' zahájena přes Python engine."}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
