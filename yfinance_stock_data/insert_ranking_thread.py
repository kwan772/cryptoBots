import os
import re
import threading
from datetime import datetime
from sqlalchemy import create_engine, text

# Set up a connection to the MySQL database

class LabelThread(threading.Thread):
    def __init__(self, id, rank, conn):
        super().__init__()
        self.id = id
        self.rank = rank
        self.conn = conn

    def run(self):
        query = text(f'''
                UPDATE new_stock_price set rank = {self.rank}
                where id = {self.id}
                ''')

        self.conn.execute(query)
        self.conn.commit()
        print(f'updated {self.id} with rank {self.rank}')


