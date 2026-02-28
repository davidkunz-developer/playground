import json
import os

def robust_inject_steps(path):
    with open(path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    # Mapping of keywords to human-readable steps
    mapping = {
        "webdriver": "Příprava prohlížeče...",
        "driver.get": "Načítám webovou stránku...",
        "preskocit_cookies": "Kontrola cookies...",
        "contact-section": "Naviguji k formuláři...",
        "firstName": "Vyplňuji jméno a příjmení...",
        "lastName": "Doplňuji údaje...",
        "phone": "Vyplňuji telefonní číslo...",
        "email": "Zadávám e-mail...",
        "message": "Píšu zprávu...",
        "submit_button": "Odesílám data...",
        "driver.save_screenshot": "Pořizuji snímek...",
        "driver.quit": "Ukončuji relaci..."
    }

    modified = False
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            source_text = "".join(cell['source'])
            
            # Skip if it already has a current_step.txt write manual OR it's just a log_result call
            if "current_step.txt" in source_text:
                continue
            
            # Determine step name
            step_name = "Pracuji na dalším kroku..."
            for key, val in mapping.items():
                if key in source_text:
                    step_name = val
                    break
            
            # Inject at the beginning of the cell
            injection = [
                f"\nwith open('current_step.txt', 'w', encoding='utf-8') as f: f.write('{step_name}')\n",
                f"print('📍 Běží: {step_name}')\n"
            ]
            cell['source'] = injection + cell['source']
            modified = True

    if modified:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=2, ensure_ascii=False)
        print(f"✅ Notebook {os.path.basename(path)} byl úspěšně vylepšen o detailní kroky.")

robust_inject_steps(r'c:\Users\Dkunz\Documents\Projekty\playground\automation_playground.ipynb')
robust_inject_steps(r'c:\Users\Dkunz\Documents\Projekty\playground\dbeaver_launcher.ipynb')
