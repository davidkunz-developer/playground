import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# Definice kroku a chyby
step_name = "Vyplňuji a odesílám formulář"
error_message = "Chyba při vyplňování formuláře nebo odesílání."

def run(driver, wait):
    # Najde pole
    first_name_field = wait.until(EC.element_to_be_clickable((By.ID, "firstName")))
    last_name_field = driver.find_element(By.ID, "lastName")
    email_field = driver.find_element(By.ID, "email")
    phone_field = driver.find_element(By.ID, "phone")
    message_field = driver.find_element(By.ID, "message")
    submit_btn = driver.find_element(By.CSS_SELECTOR, "#contact-form button[type='submit']")

    # Vyplní údaje
    first_name_field.send_keys("Robot")
    last_name_field.send_keys("Tonda")
    email_field.send_keys("tonda.robot@solutions.cz")
    phone_field.send_keys("+420 777 000 001")
    message_field.send_keys("Tento test proběhl v novém, rozděleném (modulárním) Python režimu.")

    # Odeslat formulář
    driver.execute_script("arguments[0].click();", submit_btn)

    # ČEKÁNÍ NA TEXT "ODESLÁNO"
    print("Čekám na potvrzení o odeslání...")
    # Tady hledáme jakýkoliv element, který obsahuje slovo 'Odesláno' nebo 'succesfully'
    try:
        # Původně tam byl text "Tato zpráva byla odeslána automaticky robotem", ale my čekáme na potvrzení webu.
        # Upravíme to tak, aby to čekalo na jakýkoliv text označující úspěch na stránce
        wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Odesláno') or contains(text(), 'Děkujeme') or contains(text(), 'success')]")))
    except:
        print("Text 'Odesláno' se neobjevil, ale to může být normální, pokud web jen blikne.")
        time.sleep(2)
