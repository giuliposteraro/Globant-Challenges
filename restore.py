from fastavro import reader
from sqlalchemy import create_engine
import pandas as pd
import argparse
import logging
import datetime

logging.basicConfig(filename='LOGS/restore.log', level=logging.ERROR, format="%(asctime)s %(levelname)s %(message)s")

parser = argparse.ArgumentParser()
parser.add_argument("table_name", help="name of the table to restore")
args = parser.parse_args()

engine = create_engine('sqlite:///globant.db')

path = f"AVRO/{args.table_name}.avro"

with open(path, 'rb') as dep:
    avro_reader = reader(dep)
    avro_records = list(avro_reader)

df_avro = pd.DataFrame(avro_records)

def insert_to_sql(table_name):
    df_avro.to_sql(table_name, con=engine, if_exists='append', index=False)
    engine.dispose()

if __name__ == '__main__':
 try:
    insert_to_sql(args.table_name)
 except Exception as e:
    logging.error(str(e))
    raise Exception('The id exits in the database')