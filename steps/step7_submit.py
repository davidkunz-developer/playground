import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

step_name = "Odeslat"
error_message = "Chyba při odesílání formuláře nebo čekání na potvrzení."

def run(driver, wait):
    submit_btn = driver.find_element(By.CSS_SELECTOR, "#contact-form button[type='submit']")
    driver.execute_script("arguments[0].click();", submit_btn)
    
    # Čekáme na potvrzení - podle script.js se v elementu #form-status objeví text "ODESLÁNO"
    print("Čekám na potvrzení 'ODESLÁNO'...")
    wait.until(EC.text_to_be_present_in_element((By.ID, "form-status"), "ODESLÁNO"))
    time.sleep(1)
