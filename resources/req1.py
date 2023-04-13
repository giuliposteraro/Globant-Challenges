from flask_restful import Resource
import pandas as pd
from sqlalchemy import text, create_engine
from flask import jsonify
import json
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt

engine = create_engine('sqlite:///globant.db')

class Requirement1(Resource):
    @jwt_required()
    def get(self):
        with engine.connect() as connection:
          df = pd.read_sql_query(text("SELECT * FROM view_req1"), connection)
          df.to_csv('result_req1.csv', index=False)
          json_data = df.to_json(orient='records')
        return jsonify(json.loads(json_data))
