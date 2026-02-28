import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

step_name = "Odeslat"
error_message = "Chyba při odesílání formuláře nebo čekání na potvrzení."

def run(driver, wait):
    submit_btn = driver.find_element(By.CSS_SELECTOR, "#contact-form button[type='submit']")
    driver.execute_script("arguments[0].click();", submit_btn)
    
    # Čekáme na potvrzení (obsahuje 'Odesláno' nebo 'success')
    wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Odesláno') or contains(text(), 'Děkujeme') or contains(text(), 'success')]")))
    time.sleep(1)
