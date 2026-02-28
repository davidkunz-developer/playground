from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

step_name = "Vyplnění formuláře"
error_message = "Chyba při vyplňování údajů do formuláře."

def run(driver, wait):
    first_name = wait.until(EC.element_to_be_clickable((By.ID, "firstName")))
    last_name = driver.find_element(By.ID, "lastName")
    email = driver.find_element(By.ID, "email")
    phone = driver.find_element(By.ID, "phone")
    message = driver.find_element(By.ID, "message")

    first_name.send_keys("Robot")
    last_name.send_keys("Tonda")
    email.send_keys("tonda.robot@solutions.cz")
    phone.send_keys("+420 777 123 456")
    message.send_keys("Automatický test - každý krok je samostatný skript.")
