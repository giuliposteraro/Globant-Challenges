from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)

api = Api(app)

directorio = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(directorio,'globant')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

database = SQLAlchemy(app)
Migrate(app.database)

api = Api(app)

class Saludo(Resource):
    def get(self):
        return{'saludo': 'Hola mundo'}
    
api.add_resource(Saludo, '/')

if __name__ == '__main__':
    app.run(debug=True, port=4000)