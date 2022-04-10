from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
PATH = "/Users/kevii/Downloads/chromedriver"

driver = webdriver.Chrome(PATH)

driver.get("https://coinmarketcap.com/")

try:
    tbody = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "tbody"))
    )
    rows = tbody.find_elements_by_tag_name("tr")

    row = rows[0].find_elements_by_tag_name("a")

    path = "//a[@href='{}']".format(row[0].get_attribute("href"))

    driver.get(row[0].get_attribute("href")+"historical-data/")

    time.sleep(2)
    
    button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Load More"))
    )
    button.click()

    time.sleep(5)
        
finally:
    driver.quit()
    
