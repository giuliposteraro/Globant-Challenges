from flask_restful import Resource
import pandas as pd
from sqlalchemy import text, create_engine
from flask import jsonify
import json

engine = create_engine('sqlite:///globant.db')

class Requirement2(Resource):
    def get(self):
        with engine.connect() as connection:
          df = pd.read_sql_query(text("SELECT * FROM view_req2"), connection)
          df.to_csv('result_req2.csv', index=False)
          json_data = df.to_json(orient='records')
        return jsonify(json.loads(json_data))