from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from db import db
from resources.jobs import Job, JobList
from resources.hired_employee import Employee, EmployeeList
from resources.departments import Department, DepartmentList
import pandas as pd
import models
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///globant.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

def load_departments_model():
    csv_data = pd.read_csv('CSV/departments.csv', sep=',', header=None)
    csv_data = csv_data.values.tolist()
    try:
        for i in csv_data:
            record = models.DepartmentsModel(**{
                'id' : i[0],
                'name' : i[1]
            })
            db.session.add(record) #Add all the records
            db.session.commit() #Attempt to commit all the records
    except:
        db.session.rollback()

def load_hired_employees_model():
    csv_data = pd.read_csv('CSV/hired_employees.csv', sep=',', header=None)
    csv_data = csv_data.fillna(0)
    csv_data = csv_data.values.tolist()
    try:
        for i in csv_data:
            record = models.HiredEmployeeModel(**{
                'id' : i[0],
                'name' : i[1],
                'datetime':i[2],
                'department_id':i[3],
                'jobs_id':i[4]
            })
            db.session.add(record) #Add all the records
            db.session.commit() #Attempt to commit all the records
    except:
        db.session.rollback()
        
def load_jobs_model():
    csv_data = pd.read_csv('CSV/jobs.csv', sep=',', header=None)
    csv_data = csv_data.values.tolist()
    try:
        for i in csv_data:
            record = models.JobsModel(**{
                'id' : i[0],
                'job' : i[1]
            })
            db.session.add(record) #Add all the records
            db.session.commit() #Attempt to commit all the records
    except:
        db.session.rollback()

"""
JWT related configuration. The following functions includes:
1) add claims to each jwt
2) customize the token expired error message
"""
app.config["JWT_SECRET_KEY"] = "globant"
jwt = JWTManager(app)

"""
`claims` are data we choose to attach to each jwt payload
and for each jwt protected endpoint, we can retrieve these claims via `get_jwt_claims()`
one possible use case for claims are access level control, which is shown below
"""

@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    # TODO: Read from a config file instead of hard-coding
    if identity == 1:
        return {"is_admin": True}
    return {"is_admin": False}


@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"message": "The token has expired.", "error": "token_expired"}), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return (
        jsonify(
            {"message": "Signature verification failed.", "error": "invalid_token"}
        ),
        401,
    )


@jwt.unauthorized_loader
def missing_token_callback(error):
    return (
        jsonify(
            {
                "description": "Request does not contain an access token.",
                "error": "authorization_required",
            }
        ),
        401,
    )


@jwt.needs_fresh_token_loader
def token_not_fresh_callback(jwt_header, jwt_payload):
    return (
        jsonify(
            {"description": "The token is not fresh.", "error": "fresh_token_required"}
        ),
        401,
    )


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return (
        jsonify(
            {"description": "The token has been revoked.", "error": "token_revoked"}
        ),
        401,
    )


# JWT configuration ends


#load_departments_model()
#load_hired_employees_model()
#load_jobs_model()

api.add_resource(Job, "/jobs/<string:name>")
api.add_resource(JobList, "/jobs")
api.add_resource(Employee, "/employees/<string:name>")
api.add_resource(EmployeeList, "/employees")
api.add_resource(Department, "/departments/<string:name>")
api.add_resource(DepartmentList, "/departments")

    