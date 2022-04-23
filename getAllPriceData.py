

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

coinList = pd.read_csv('coinList.csv')
coinList.reset_index()
for index,row in coinList.iterrows():
    if index>=303:
        print(row["Coin name"])

        path = "https://www.coingecko.com/en/coins/"+row["Coin name"]+"/historical_data/usd?start_date=2019-03-01&end_date=2022-04-10#panel"

        driver.get(path)

        tbody = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "tbody"))
        )
        dd = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "dropdown"))
        )

        button = driver.find_element_by_xpath("//div[@class='coingecko-table table-responsive']")
        b = button.find_element_by_tag_name('button')

        b.click()

        a = button.find_element_by_link_text('CSV')
        href = a.get_attribute("href")

        print(path)
        print(href)

        c = requests.get(href)
        cc = StringIO(c.text)
        df = pd.read_csv(cc)

        filename = row['Coin name']+".csv"
        df.to_csv(filename,index=False)
