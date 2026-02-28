from fastapi import FastAPI, BackgroundTasks, Header, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
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
        return JSONResponse(content={"step": "Čekám na instrukce..."})
    try:
        with open("current_step.txt", "r", encoding="utf-8") as f:
            return JSONResponse(content={"step": f.read()})
    except:
        return JSONResponse(content={"step": "Pracuji..."})

@app.post("/run/{notebook_id}")
async def run_automation(notebook_id: str, api_key: str = Depends(verify_api_key)):
    if notebook_id not in NOTEBOOKS:
        return JSONResponse(content={"status": "error", "message": f"Notebook '{notebook_id}' nebyl nalezen."}, status_code=404)
    
    # Reset statusu na začátku
    with open("current_step.txt", "w", encoding="utf-8") as f: 
        f.write("Příprava notebooku k běhu...")

    notebook_file = NOTEBOOKS[notebook_id]
    try:
        # Výstupní notebook uložíme do dočasného souboru
        output_path = os.path.join(os.environ.get('TEMP', '/tmp'), f"executed_{notebook_id}_{int(time.time())}.ipynb")
        pm.execute_notebook(
            notebook_file,
            output_path,
            parameters={} 
        )
        # Smažeme status po dokončení
        if os.path.exists("current_step.txt"): os.remove("current_step.txt")
        return {"status": "success", "message": f"Notebook '{notebook_id}' byl úspěšně spuštěn."}
    except Exception as e:
        if os.path.exists("current_step.txt"): os.remove("current_step.txt")
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
