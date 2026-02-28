from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

step_name = "scroll na sekci Kontkaty"
error_message = "Nepodařilo se najít nebo prescrollovat na sekci Kontakty."

def run(driver, wait):
    contact_section = wait.until(EC.presence_of_element_located((By.ID, "contact-section")))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});", contact_section)
