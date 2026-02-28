import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait

step_name = "spuštění prohlížeče"
error_message = "Nepodařilo se spustit prohlížeč Chrome."

def run():
    os.environ['WDM_LOG_LEVEL'] = '0'
    os.environ['WDM_LOCAL_PATH'] = os.path.join(os.getcwd(), ".wdm")

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    
    # Zakázání obrázků pro rychlost
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(10)
    wait = WebDriverWait(driver, 10)
    
    return driver, wait
