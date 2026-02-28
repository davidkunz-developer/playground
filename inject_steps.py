import json
import os

def update_notebook_with_steps(path):
    with open(path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    # Define steps mapping for specific cells based on content
    steps = {
        "webdriver": "Otevírám prohlížeč Chrome...",
        "driver.get": "Naviguji na webovou stránku...",
        "preskocit_cookies": "Potvrzuji cookies...",
        "contact-section": "Hledám sekci Kontakt...",
        "firstName": "Vyplňuji kontaktní formulář...",
        "submit_button.click": "Odesílám formulář...",
        "driver.quit": "Ukončuji prohlížeč a ukládám výsledek..."
    }

    def set_step_code(step_name):
        return f"\nwith open('current_step.txt', 'w', encoding='utf-8') as f: f.write('{step_name}')\nprint('📍 Aktuální krok: {step_name}')\n"

    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            source = "".join(cell['source'])
            for key, msg in steps.items():
                if key in source and "current_step.txt" not in source:
                    cell['source'] = [set_step_code(msg)] + cell['source']
                    break

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=2, ensure_ascii=False)

update_notebook_with_steps(r'c:\Users\Dkunz\Documents\Projekty\playground\automation_playground.ipynb')
print("Notebook updated with real-time status reporting.")
