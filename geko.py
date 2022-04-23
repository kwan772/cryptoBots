from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import pandas as pd
from io import StringIO


PATH = "/Users/kevii/Downloads/chromedriver"

driver = webdriver.Chrome(PATH)

driver.get("https://www.coingecko.com/en/coins/ethereum/historical_data/usd?start_date=2019-03-01&end_date=2022-04-10#panel")

tbody = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.TAG_NAME, "tbody"))
)
dd = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "dropdown"))
)

button = driver.find_element_by_xpath("//div[@class='coingecko-table table-responsive']")
print(button)
print(button.text)
b = button.find_element_by_tag_name('button')

print(b.text)
b.click()

a = button.find_element_by_link_text('CSV')
href = a.get_attribute("href")
print(href)

c = requests.get(href)
print(c.text)
cc = StringIO(c.text)
df = pd.read_csv(cc)
df.to_csv('eth.csv',index=False)
