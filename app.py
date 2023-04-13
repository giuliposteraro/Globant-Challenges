from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from db import db
from resources.jobs import Job, JobList
from resources.hired_employee import Employee, EmployeeList
from resources.departments import Department, DepartmentList
from resources.req1 import Requirement1
from resources.req2 import Requirement2
from flask_migrate import Migrate
from resources.users import UserRegister, UserLogin, User, TokenRefresh, UserLogout
from blocklist import BLOCKLIST
import os

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
with app.app_context():
    db.create_all()
    app.debug = True
# JWT configuration ends

api.add_resource(Job, "/jobs/<string:name>")
api.add_resource(JobList, "/jobs")
api.add_resource(Employee, "/employees/<string:name>")
api.add_resource(EmployeeList, "/employees")
api.add_resource(Department, "/departments/<string:name>")
api.add_resource(DepartmentList, "/departments")
api.add_resource(Requirement1, "/requirement1")
api.add_resource(Requirement2, "/requirement2")
api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")
api.add_resource(UserLogout, "/logout")
api.add_resource(User, "/user/<int:user_id>")
