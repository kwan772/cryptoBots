from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
import pandas as pd
from io import StringIO

import numpy as np

from bs4 import BeautifulSoup

coinBase = []

for i in range(1,31):

    src = "https://www.coingecko.com/?page="+str(i)
    page = requests.get(src)

    soup = BeautifulSoup(page.content, 'html.parser')

    trs = soup.find_all("tr")

    for tr in trs[1:]:
        tds = tr.find_all("td")
        a = tds[2].find_all("a")
        coinBase.append([tds[1].string.strip().lower().replace('.','').replace(' ','-'),a[0].string.strip().lower().replace('.','').replace(' ','-')])



df = pd.DataFrame(np.array(coinBase),columns=['Coin number', 'Coin name'])
print(df)
df.to_csv('coinList.csv',index=False)


