from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError
from models import DepartmentsModel


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
        return {"message": "Department not found"}, 404

    @jwt_required(fresh=True)
    def post(self, name):
        if DepartmentsModel.find_by_name(name):
            return {
                "message": "A department with name '{}' already exists.".format(name)
            }, 400

        data = self.parser.parse_args()

        department = DepartmentsModel(name=name, **data)

        try:
            department.save_to_db()
        except SQLAlchemyError:
            return {"message": "An error occurred while inserting the item."}, 500

        return department.json(), 201

    @jwt_required()
    def delete(self, name):
        jwt = get_jwt()
        if not jwt["is_admin"]:
            return {"message": "Admin privilege required."}, 401

        department = DepartmentsModel.find_by_name(name)
        if department:
            department.delete_from_db()
            return {"message": "Department deleted."}
        return {"message": "Department not found."}, 404

    def put(self, name):
        data = self.parser.parse_args()

        department = DepartmentsModel.find_by_name(name)

        if department:
            department.department = data["department"]
        else:
            department = DepartmentsModel(name, **data)

        department.save_to_db()

        return department.json()


class DepartmentList(Resource):
    @jwt_required(optional=True)
    def get(self):
        user_id = get_jwt_identity()
        departments = [department.json() for department in DepartmentsModel.find_all()]
        if user_id:
            return {"items": departments}, 200
        return {
            "departments": [department["name"] for department in departments],
            "message": "More data available if you log in.",
        }, 200