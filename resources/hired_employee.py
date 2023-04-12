from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError
from models import HiredEmployeeModel


class Employee(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "employee", type=str, required=True, help="This field cannot be left blank!"
    )

    @jwt_required()
    def get(self, name):
        employee = HiredEmployeeModel.find_by_name(name)
        if employee:
            return employee.json()
        return {"message": "Hired Employee not found"}, 404

    @jwt_required(fresh=True)
    def post(self, name):
        if HiredEmployeeModel.find_by_name(name):
            return {
                "message": "An employee with name '{}' already exists.".format(name)
            }, 400

        data = self.parser.parse_args()

        employee = HiredEmployeeModel(name=name, **data)

        try:
            employee.save_to_db()
        except SQLAlchemyError:
            return {"message": "An error occurred while inserting the item."}, 500

        return employee.json(), 201

    @jwt_required()
    def delete(self, name):
        jwt = get_jwt()
        if not jwt["is_admin"]:
            return {"message": "Admin privilege required."}, 401

        employee = HiredEmployeeModel.find_by_name(name)
        if employee:
            employee.delete_from_db()
            return {"message": "Employee deleted."}
        return {"message": "Employee not found."}, 404

    def put(self, name):
        data = self.parser.parse_args()

        employee = HiredEmployeeModel.find_by_name(name)

        if employee:
            employee.employee = data["employee"]
        else:
            employee = HiredEmployeeModel(name, **data)

        employee.save_to_db()

        return employee.json()


class EmployeeList(Resource):
    @jwt_required(optional=True)
    def get(self):
        user_id = get_jwt_identity()
        employees = [employee.json() for employee in HiredEmployeeModel.find_all()]
        if user_id:
            return {"items": employees}, 200
        return {
            "employees": [employee["name"] for employee in employees],
            "message": "More data available if you log in.",
        }, 200