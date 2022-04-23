import requests

c = requests.get("https://www.coingecko.com/price_charts/export/10365/usd.csv")


print(c)
