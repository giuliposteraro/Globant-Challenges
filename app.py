from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from db import db
from resources.jobs import Job, JobList, UpdateJob
from resources.hired_employee import Employee, EmployeeList, UpdateEmployee
from resources.departments import Department, DepartmentList, UpdateDepartment
from resources.req1 import Requirement1
from resources.req2 import Requirement2
from flask_migrate import Migrate
from resources.users import UserRegister, UserLogin, User, TokenRefresh, UserLogout
from blocklist import BLOCKLIST
import os
import logging

logging.basicConfig(filename='LOGS/api.log', level=logging.ERROR, format="%(asctime)s %(levelname)s %(message)s")

app = Flask(__name__, instance_path=os.getcwd())

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///globant.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

"""
JWT related configuration. The following functions includes:
1) add claims to each jwt
2) customize the token expired error message
"""
app.config["JWT_SECRET_KEY"] = "globant"
jwt = JWTManager(app)

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    logging.error("token_expired")
    return jsonify({"message": "The token has expired.", "error": "token_expired"}), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    logging.error(str(error))
    return (
        jsonify(
            {"message": "Signature verification failed.", "error": "invalid_token"}
        ),
        401,
    )


@jwt.unauthorized_loader
def missing_token_callback(error):
    logging.error(str(error))
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
    logging.error("fresh_token_required")
    return (
        jsonify(
            {"description": "The token is not fresh.", "error": "fresh_token_required"}
        ),
        401,
    )


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    logging.error("token_revoked")
    return (
        jsonify(
            {"description": "The token has been revoked.", "error": "token_revoked"}
        ),
        401,
    )
with app.app_context():
    db.create_all()

api.add_resource(Job, "/jobs/<string:job>")
api.add_resource(JobList, "/jobs")
api.add_resource(UpdateJob, "/jobs/<int:id>")

api.add_resource(Employee, "/employees/<string:name>")
api.add_resource(EmployeeList, "/employees")
api.add_resource(UpdateEmployee, "/employees/<int:id>")

api.add_resource(Department, "/departments/<string:name>")
api.add_resource(DepartmentList, "/departments")
api.add_resource(UpdateDepartment, "/departments/<int:id>")

api.add_resource(Requirement1, "/requirement1")
api.add_resource(Requirement2, "/requirement2")


api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")
api.add_resource(UserLogout, "/logout")
api.add_resource(User, "/user/<int:user_id>")
