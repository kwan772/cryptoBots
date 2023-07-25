import os
from insert_ranking_thread import LabelThread

from sqlalchemy import create_engine, text

db_connection_str = 'mysql+pymysql://root:' + os.getenv('DB_PASSWORD') + '@localhost/stock_data'
engine = create_engine(db_connection_str)

with engine.connect() as conn:
    query = text(f'''
    CREATE TEMPORARY TABLE temp_stocks_ranked AS
    SELECT 
      id as new_id, 
      date(date) as d, 
      RANK() OVER (
        PARTITION BY date(date)
        ORDER BY `next_day_change_percentage` DESC
      ) AS ranking
    FROM new_stock_price;
    ''')
    conn.execute(query)
    conn.commit()

with engine.connect() as conn:
    # batch_size = 1000  # Number of rows to update in each batch
    # offset = 393000
    #
    # while offset < 8600742:
    #
    #     print('processed ' + str(offset) + 'rows')
    #     query = text(f'''
    #     UPDATE new_stock_price AS a
    #     JOIN (
    #     SELECT new_id, ranking
    #     FROM temp_stocks_ranked
    #     ORDER BY new_id
    #     LIMIT {batch_size} OFFSET {offset}
    #     ) AS b ON a.id = b.new_id
    #     SET a.rank = b.ranking
    #     ''')
    #
    #     conn.execute(query)
    #     offset += batch_size
    rows_processed = 393000

    query = text(f'''
    select new_id, ranking from new_stock_price a 
    join temp_stocks_ranked b 
    on a.id = b.new_id
    order by new_id
    limit 10000000 offset 393000
    ''')

    results = conn.execute(query)
    results = results.fetchall()
    conn.commit()

    for row in results:
        thread = LabelThread(row['new_id'], row['ranking'], conn)
        thread.run()
        rows_processed+=1
        print(rows_processed)
