import pandas as pd
import glob
from datetime import datetime
from datetime import date



def combine(number_of_rows, directory):

    all_csv = glob.glob(directory+'/*.csv')
    df_list = []
    combine_df = []

    for file_name in all_csv:
        df = pd.read_csv(file_name)
        if len(df) == number_of_rows:
            df_list.append(df)
        print(len(df))

    for i in range(0, number_of_rows):
        for x in range(0, len(df_list)):
            df = df_list[x]
            # print(all_csv[x])
            # print(x)
            # print(i)
            combine_df.append([df.iloc[i]['snapped_at'], df.iloc[i]['market_cap'], df.iloc[i]['Pre Change'],
                               df.iloc[i]['Post Change']])

    print(len(df_list))

    combine_df = pd.DataFrame(combine_df, columns=['snapped_at', 'market_cap', 'Pre Change', 'Post Change'])
    combine_df.to_csv(directory+'combined.csv', index=False)

if __name__ == '__main__':

    all_csv = glob.glob('CoinData/*.csv')
    total = 0
    old = 0


    for file_name in all_csv:
        df = pd.read_csv(file_name)

        dt_str = df.iloc[0].snapped_at[0:10]

        dt_obj = datetime.strptime(dt_str, '%Y-%m-%d')

        start_date = datetime(2016,1,1)
        end_date = date.today()

        total += 1

        if start_date >= dt_obj:
            old += 1
            start_index = 0
            for index, row in df.iterrows():
                if df.iloc[index].snapped_at[0:10] == "2016-01-01":
                    start_index = index
                    break
            df = df.iloc[start_index:]
            df.to_csv('six_year_coins'+file_name[8:], index=False)

    combine(2303, 'six_year_coins')

