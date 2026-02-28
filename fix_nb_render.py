import json
import sys

path = r'c:\Users\Dkunz\Documents\Projekty\playground\automation_playground.ipynb'
with open(path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Modify the selenium cell to be more robust for Render
cell = nb['cells'][2]
new_source = [
    "status = \"error\"\n",
    "error_message = \"Nepovedlo se mi otevřít Selenium\"\n",
    "\n",
    "from selenium import webdriver\n",
    "from selenium.webdriver.chrome.service import Service\n",
    "from selenium.webdriver.chrome.options import Options\n",
    "from selenium.webdriver.common.by import By\n",
    "from webdriver_manager.chrome import ChromeDriverManager\n",
    "import time\n",
    "import sys\n",
    "import os\n",
    "\n",
    "print(\"🔧 Spouštím Chrome...\")\n",
    "chrome_options = Options()\n",
    "chrome_options.add_argument(\"--start-maximized\")\n",
    "\n",
    "if sys.platform != \"win32\":\n",
    "    print(\"🐧 Detekován Linux (Render)\")\n",
    "    chrome_options.add_argument(\"--headless\")\n",
    "    chrome_options.add_argument(\"--no-sandbox\")\n",
    "    chrome_options.add_argument(\"--disable-dev-shm-usage\")\n",
    "    # Zkusíme explicitně nastavit cestu k binárce, která se v Dockeru vytvoří\n",
    "    if os.path.exists(\"/usr/bin/google-chrome\"):\n",
    "        chrome_options.binary_location = \"/usr/bin/google-chrome\"\n",
    "\n",
    "try:\n",
    "    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)\n",
    "    print(\"✅ Prohlížeč je připraven.\")\n",
    "except Exception as e:\n",
    "    error_message = f\"Chyba při startu Chromu: {str(e)}\"\n",
    "    print(f\"❌ {error_message}\")\n",
    "    raise e"
]

cell['source'] = new_source

with open(path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=2, ensure_ascii=False)
