import json
import os

def update_notebook_with_screenshot(path):
    with open(path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    # Update logging function to accept screenshot
    # And add driver.save_screenshot logic
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            source = "".join(cell['source'])
            
            # Update log_result definition
            if 'def log_result(rid, msg, st):' in source:
                cell['source'] = source.replace(
                    'def log_result(rid, msg, st):',
                    'def log_result(rid, msg, st, ss=""):').replace(
                    'header = ["id_behu", "datum", "cas", "error_message", "status"]',
                    'header = ["id_behu", "datum", "cas", "error_message", "status", "screenshot"]').replace(
                    'new_entry = [rid, now.strftime("%d.%m.%Y"), now.strftime("%H:%M:%S"), msg, st]',
                    'new_entry = [rid, now.strftime("%d.%m.%Y"), now.strftime("%H:%M:%S"), msg, st, ss]'
                ).splitlines(keepends=True)
            
            # Add screenshot capture before closing browser
            if 'driver.quit()' in source:
                screenshot_logic = [
                    "\n",
                    "# --- POŘÍZENÍ SCREENSHOTU ---\n",
                    "ss_dir = \"screenshots\"\n",
                    "if not os.path.exists(ss_dir): os.makedirs(ss_dir)\n",
                    "ss_name = f\"screenshot_{run_id}.png\"\n",
                    "ss_path = os.path.join(ss_dir, ss_name)\n",
                    "try:\n",
                    "    driver.save_screenshot(ss_path)\n",
                    "    screenshot_url = f\"/screenshots/{ss_name}\"\n",
                    "    print(f\"📸 Screenshot uložen: {ss_path}\")\n",
                    "except Exception as e:\n",
                    "    print(f\"❌ Chyba při focení: {e}\")\n",
                    "    screenshot_url = \"\"\n",
                    "\n"
                ]
                new_source = source.replace('driver.quit()', "".join(screenshot_logic) + 'driver.quit()')
                # Update the final log_result call
                new_source = new_source.replace('log_result(run_id, error_message, status)', 'log_result(run_id, error_message, status, screenshot_url)')
                cell['source'] = new_source.splitlines(keepends=True)

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=2, ensure_ascii=False)

# Update the main automation notebook
update_notebook_with_screenshot(r'c:\Users\Dkunz\Documents\Projekty\playground\automation_playground.ipynb')
print("Notebook updated with screenshot logic.")
