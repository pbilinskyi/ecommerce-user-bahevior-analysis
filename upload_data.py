import os
import logging

import duckdb


logging.basicConfig(level='DEBUG', format='%(message)s')


dataset_fname = os.path.join('data', '2019-Nov.csv')

# connect to local datavase
con = duckdb.connect('ecommerce_store.duckdb')
logging.info('SUCCESS: Connected to DuckDB database')

# Upload dataset to DuckDB database:
logging.info('STARTED: uploding data to database')
query = """
create table user_event AS
select *
from read_csv($dataset_fname,
              header=true,
              columns={
                'event_time': 'TIMESTAMP',
                'event_type': 'VARCHAR',
                'product_id': 'INTEGER',
                'category_id': 'BIGINT',
                'category_code': 'VARCHAR',
                'brand': 'VARCHAR',
                'price': 'DOUBLE',
                'user_id': 'INTEGER',
                'user_session': 'VARCHAR'
              },
              timestampformat='%c UTC'
              );
"""
con.execute(query=query, parameters={"dataset_fname": dataset_fname})

# check if data were uploaded:
records_num = con.execute('select count(*) as event_cnt from user_event').fetchone()[0]
logging.info(('SUCCESS' if records_num == 67501979 else 'FAILED') + ': uploading data to database.')
logging.info(f'Number of records in table user_event is {records_num}, should be 67501979')
