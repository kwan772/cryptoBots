from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
PATH = "/Users/kevii/Downloads/chromedriver"

driver = webdriver.Chrome(PATH)

driver.get("https://coinmarketcap.com/currencies/bitcoin/historical-data/")

try:
    tbody = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "b4d71h-0"))
    )
    print(tbody.text)

    time.sleep(5)
    
    button = tbody.find_elements(By.TAG_NAME,"button")
    print(button.text)
    print(button)
    print(@@@@@@@@@@@@@)
    time.sleep(5)
        
finally:
    driver.quit()
    
