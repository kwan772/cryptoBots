import os
import re
import threading
from datetime import datetime
from sqlalchemy import create_engine, text

class LabelThread(threading.Thread):
    def __init__(self, id, rank, db_connection_str):
        super().__init__()
        self.id = id
        self.rank = rank
        self.db_connection_str = db_connection_str

    def run(self):
        engine = create_engine(self.db_connection_str)
        with engine.connect() as conn:
            query = text(f'''
                UPDATE new_stock_price SET `rank` = {self.rank}
                WHERE id = {self.id}
            ''')
            conn.execute(query)
            conn.commit()
            print(f'Updated {self.id} with rank {self.rank}')


if __name__ == '__main__':
    db_password = os.getenv('DB_PASSWORD')
    db_connection_str = f'mysql+pymysql://root:{db_password}@localhost/stock_data'
    engine = create_engine(db_connection_str)

    with engine.connect() as conn:
        query = text('''
            CREATE TEMPORARY TABLE temp_stocks_ranked AS
            SELECT 
              id AS new_id, 
              RANK() OVER (
                PARTITION BY date(date)
                ORDER BY `next_day_change_percentage` DESC
              ) AS ranking
            FROM new_stock_price
            ORDER BY id
        ''')
        conn.execute(query)
        conn.commit()

    batch_size = 450
    offset = 0
    total_rows = 8600742

    while offset < total_rows:
        with engine.connect() as conn:
            query = text(f'''
                SELECT new_id, ranking
                FROM temp_stocks_ranked
                LIMIT {batch_size} OFFSET {offset}
            ''')
            results = conn.execute(query).fetchall()

        threads = []
        for row in results:
            thread = LabelThread(row[0], row[1], db_connection_str)
            threads.append(thread)

        # Start the threads
        for thread in threads:
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        offset += batch_size
        print(f"row processed {offset}")
