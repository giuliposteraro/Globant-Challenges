from fastavro import writer, parse_schema, schema
import pandas as pd
from db import db
from sqlalchemy import create_engine, text, inspect
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("table_name", help="name of the table to do a backup")
args = parser.parse_args()
engine = create_engine('sqlite:///globant.db')

schema_departments = {
    'doc': 'departments',
    'name': 'departments',
    'namespace': 'departments',
    'type': 'record',
    'fields': [
        {'name': 'id', 'type': 'int'},
        {'name': 'name', 'type': ['string', 'null']}
    ]
}
parsed_departments = parse_schema(schema_departments)

schema_jobs = {
    'doc': 'jobs',
    'name': 'jobs',
    'namespace': 'jobs',
    'type': 'record',
    'fields': [
        {"name": "id", "type": "int"},
        {"name": "job", "type": "string"}
    ]
}

parsed_jobs = parse_schema(schema_jobs)

schema_hired_employees = {
    'doc': 'hired_employees',
    'name': 'hired_employees',
    'namespace': 'hired_employees',
    'type': 'record',
    'fields': [
        {'name': 'id', 'type': 'int'},
        {'name': 'name', 'type': 'string'},
        {'name': 'datetime', 'type': 'string'},
        {'name': 'department_id', 'type': 'int'},
        {'name': 'jobs_id', 'type': ['int', 'null']},
    ]
}

parsed_hired_employees = parse_schema(schema_hired_employees)

inspector = inspect(engine)
# Get a list of all the table names in the database
table_names = inspector.get_table_names()

def sql_to_avro(table):
    with engine.connect() as connection:
        query = f'SELECT * FROM {table}'
        df = pd.read_sql_query(text(query), connection)
        records = df.to_dict('records')
        filename = f"AVRO/{table}.avro"
        with open(filename, 'wb') as out:
           if table == 'departments':
             writer(out, parsed_departments, records)
           elif table == 'jobs':
              writer(out, parsed_jobs, records)
           else:
              writer(out, parsed_hired_employees, records)
              

if __name__ == '__main__':
    try:
     sql_to_avro(args.table_name)
    except:
      if args.table_name not in table_names:
         raise Exception('The table does not exist in database')