import json
import os

def optimize_notebook_for_ram(path):
    with open(path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            source = "".join(cell['source'])
            
            # Najdeme místo, kde se nastavují chrome_options
            if 'chrome_options = Options()' in source:
                # Přidáme extrémně úsporné parametry
                ram_saving_flags = [
                    "    chrome_options.add_argument(\"--disable-gpu\")\n",
                    "    chrome_options.add_argument(\"--disable-extensions\")\n",
                    "    chrome_options.add_argument(\"--no-zygote\")\n",
                    "    chrome_options.add_argument(\"--single-process\")\n", # Klíčové pro RAM
                    "    chrome_options.add_argument(\"--disable-dev-shm-usage\")\n"
                ]
                
                # Vložíme tyto flagy do buňky
                new_source = source.replace('chrome_options = Options()', 'chrome_options = Options()\n' + "".join(ram_saving_flags))
                cell['source'] = new_source.splitlines(keepends=True)
                
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=2, ensure_ascii=False)

optimize_notebook_for_ram(r'c:\Users\Dkunz\Documents\Projekty\playground\automation_playground.ipynb')
print("Notebook optimized for low-RAM environments.")
