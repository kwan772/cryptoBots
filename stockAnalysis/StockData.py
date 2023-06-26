import math

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import glob
from datetime import datetime
from datetime import date
import os


class StockData:
    PATH = "./../chromedriver"

    chrome_options = webdriver.ChromeOptions()

    chrome_options.binary_location = "/Applications/Google Chrome Beta.app/Contents/MacOS/Google Chrome Beta"

    all_csv = sorted(glob.glob('./stockData/stock-historical-price/*.csv'), key=os.path.getmtime)

    @staticmethod
    def getAllPriceData():
        driver = webdriver.Firefox()
        file = open("./stockData/stockList.txt", "a")

        coinList = pd.read_csv('./stockData/nasdaq_screener_1657171802607.csv')
        coinList.reset_index()
        startLoop = False
        count = 0


        for index, row in coinList.iterrows():
            # if row['Symbol'] == 'CCNC':
            #     startLoop = True
            #
            # if row['Symbol'] == 'CENX':
            #     startLoop = False

            if startLoop and not math.isnan(row['IPO Year']) and int(row['IPO Year']) < 2005:
                path = "https://www.nasdaq.com/market-activity/stocks/" + row[
                    "Symbol"] + "/historical"

                driver.get(path)
                driver.maximize_window()

                max_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//button[@class='table-tabs__tab'][5]"))
                )
                max_button.location_once_scrolled_into_view
                time.sleep(1)

                result = None
                while result is None:
                    try:
                        max_button.click()
                        result = 1
                    except:
                        time.sleep(1)

                downloadButton = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//button[@class='historical-data__controls-button--download historical-download'][1]"))
                )

                result = None
                while result is None:
                    try:
                        downloadButton.click()
                        time.sleep(2)
                        result = 1
                        file.write(row["Name"] + ',')
                        print(row["Name"] + ',')
                        count += 1
                        print(count + ". " + row["Name"] + ',')
                    except:
                        time.sleep(1)

            if row['Symbol'] == 'HNP':
                startLoop = True

        file.close()

    @staticmethod
    def cutTimeCSV():
            # total = 0
            # old = 0
            # name_list = []
            # with open("./stockData/newStockList.txt","r+") as stock_list:
            #     name_list_str = stock_list.readline()
            #     name_list = name_list_str.split(',')


            for index, file_name in enumerate(StockData.all_csv):
                df = pd.read_csv(file_name)

                if df.size == 15090:
                    print(file_name[35:])
                    df.to_csv('stockData/stock-historical-price/2012-historical-data/' + file_name[35:], index=False)


                # dt_obj = datetime.strptime(dt_str, '%m/%d/%Y')
                #
                # start_date = datetime(year, month, day)
                # end_date = date.today()
                #
                # total += 1
                #
                # if start_date >= dt_obj:
                #     old += 1
                #     end_index = 0
                #     for index, row in df.iterrows():
                #         if df.iloc[index].snapped_at[0:10] == "2020-01-01":
                #             start_index = index
                #             break
                #     df = df.iloc[start_index:]
                #     print(file_name)
                #     print(df)
                # df.to_csv('stockData/stock-historical-price' + file_name[8:], index=False)
                #     stop = True


    @staticmethod
    def calcPriceChange():

        price_2012_csv = sorted(glob.glob('./stockData/stock-historical-price/2012-historical-data/*.csv'), key=os.path.getmtime)

        for file_name in price_2012_csv:

            df = pd.read_csv(file_name)

            if 'Pre Change' not in df.columns:
                pre_changes = [0]
                post_changes = []

                for index, row in df.iterrows():
                    if index > 0:
                        post_changes.append((float(df.loc[index-1]['Close/Last'][1:]) - float(
                        df.loc[index]['Close/Last'][1:])) / float(df.loc[index]['Close/Last'][1:]))
                    if index < len(df) - 1:
                        pre_changes.append((float(df.loc[index]['Close/Last'][1:]) - float(
                        df.loc[index+1]['Close/Last'][1:])) / float(df.loc[index+1]['Close/Last'][1:]))

                post_changes.append(0)

                df.insert(loc=2, column='Pre Change', value=pre_changes)
                df.insert(loc=2, column='Post Change', value=post_changes)
                df = df.iloc[1:-1]
                df.to_csv(file_name, index=False)
                print(df[['Close/Last', 'Pre Change', 'Post Change']])

        print("safely done")

    @staticmethod
    def updatePriceChange():

        price_2012_csv = sorted(glob.glob('./stockData/stock-historical-price/2012-historical-data/*.csv'),
                                key=os.path.getmtime)

        for file_name in price_2012_csv:

            df = pd.read_csv(file_name)

            for index, row in df.iterrows():
                if index > 0:
                    v = (float(df.loc[index-1]['Close/Last'][1:]) - float(
                        df.loc[index]['Close/Last'][1:])) / float(df.loc[index]['Close/Last'][1:])
                    df.at[index,"Post Change"] = v
                if index < len(df) - 1:
                    v = (float(df.loc[index]['Close/Last'][1:]) - float(
                        df.loc[index+1]['Close/Last'][1:])) / float(df.loc[index+1]['Close/Last'][1:])
                    df.at[index,"Pre Change"] = v

            df = df.iloc[1:-1]
            df.to_csv(file_name, index=False)
            print(df[['Close/Last', 'Pre Change', 'Post Change']])

        print("safely done")

    @staticmethod
    def combinePriceData(days):

        all_csv_from_time = glob.glob('./stockData/stock-historical-price/2012-historical-data/*.csv')
        df_list = []
        combine_df = []

        for file_name in all_csv_from_time:
            df = pd.read_csv(file_name)
            print(len(df))
            if len(df) == days:
                df_list.append(df)

        print("@@@@@@@@@@@@@@")
        print(len(df_list))

        for i in range(0, days):
            for x in range(0, len(df_list)):
                df = df_list[x]
                # print(all_csv[x])
                # print(x)
                # print(i)
                print([df.iloc[i]['Date'], df.iloc[i]['Close/Last'], df.iloc[i]['Pre Change'],
                       df.iloc[i]['Post Change']])
                combine_df.append([df.iloc[i]['Date'], df.iloc[i]['Close/Last'], df.iloc[i]['Pre Change'],
                       df.iloc[i]['Post Change']])

        print(combine_df)
        print(len(combine_df))

        combine_df = pd.DataFrame(combine_df, columns=['Date', 'Close/Last', 'Pre Change', 'Post Change'])
        combine_df.to_parquet('./stockData/combined'+str(days)+'days.parquet', index=False)
