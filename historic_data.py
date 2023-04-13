import pandas as pd
import argparse
from sqlalchemy import create_engine
import logging

logging.basicConfig(filename='LOGS/historic_data.log', level=logging.ERROR, format="%(asctime)s %(levelname)s %(message)s")

parser = argparse.ArgumentParser()
parser.add_argument("table_name", help="name of the table to load")
args = parser.parse_args()

def load_model(table):
    path = f"CSV/{table}.csv"

    if table == 'departments':
        col_names = ['id', 'name']
    elif table == 'jobs':
        col_names = ['id', 'job']
    else:
        col_names = ['id', 'name', 'datetime', 'department_id', 'jobs_id']

    df = pd.read_csv(path, sep=',', header=None, names=col_names)

    df.to_sql(table, con=engine, if_exists='append', index=False)


if __name__ == '__main__':
    engine = create_engine('sqlite:///instance/globant.db')
    try: 
        load_model(args.table_name)
        engine.dispose()
    except Exception as e:
        logging.error(str(e))
        raise Exception('Id actually exists in database')