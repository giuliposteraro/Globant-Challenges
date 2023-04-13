from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError
from models import DepartmentsModel
import logging

logging.basicConfig(filename='LOGS/api.log', level=logging.ERROR, format="%(asctime)s %(levelname)s %(message)s")

class Department(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "department", type=str, required=True, help="This field cannot be left blank!"
    )

    @jwt_required()
    def get(self, name):
        department = DepartmentsModel.find_by_name(name)
        if department:
            return department.json()
        else:
            logging.error("Department not found")
        return {"message": "Department not found"}, 404

    @jwt_required(fresh=True)
    def post(self, name):
        if DepartmentsModel.find_by_name(name):
            logging.error("A department with name '{}' already exists.".format(name))
            return {
                "message": "A department with name '{}' already exists.".format(name)
            }, 400

        data = self.parser.parse_args()

        name = DepartmentsModel(**data)

        try:
            name.save_to_db()
        except SQLAlchemyError as e:
            logging.error(str(e))
            return {"message": "An error occurred while inserting the item."}, 500

        return name.json(), 201

    @jwt_required()
    def delete(self, name):
        # jwt = get_jwt()
        # if not jwt["is_admin"]:
        #     return {"message": "Admin privilege required."}, 401

        department = DepartmentsModel.find_by_name(name)
        if department:
            department.delete_from_db()
            return {"message": "Department deleted."}
        else:
            logging.error("Department not found.")
        return {"message": "Department not found."}, 404
    
class UpdateDepartment(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "department", type=str, required=True, help="This field cannot be left blank!"
    )
    @jwt_required(fresh=True)
    def put(self, id):
        data = self.parser.parse_args()

        department = DepartmentsModel.find_by_id(id)

        if department:
            department.department = data["department"]
            department.save_to_db()
        else:
            logging.error("Department doesn't exist")
            return {"message": "Department doesn't exist"}

        return department.json()

class DepartmentList(Resource):
    @jwt_required(optional=True)
    def get(self):
        user_id = get_jwt_identity()
        departments = [department.json() for department in DepartmentsModel.find_all()]
        if user_id:
            return {"departments": [{"id": department["id"],"name": department["name"]} for department in departments]}, 200
        else:
            return {
            "message": "More data available if you log in.",
        }, 400