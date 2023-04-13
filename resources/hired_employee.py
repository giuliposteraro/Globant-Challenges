from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError
from models import HiredEmployeeModel
import logging

logging.basicConfig(filename='LOGS/api.log', level=logging.ERROR, format="%(asctime)s %(levelname)s %(message)s")

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
        else:
            logging.error("Hired Employee not found")
        return {"message": "Hired Employee not found"}, 404

    @jwt_required(fresh=True)
    def post(self, name):
        if HiredEmployeeModel.find_by_name(name):
            logging.error("An employee with name '{}' already exists.".format(name))
            return {
                "message": "An employee with name '{}' already exists.".format(name)
            }, 400

        data = self.parser.parse_args()

        employee = HiredEmployeeModel(**data)

        try:
            employee.save_to_db()
        except SQLAlchemyError as e:
            logging.error(str(e))
            return {"message": "An error occurred while inserting the item."}, 500

        return employee.json(), 201

    @jwt_required()
    def delete(self, name):
        # jwt = get_jwt()
        # if not jwt["is_admin"]:
        #     return {"message": "Admin privilege required."}, 401

        employee = HiredEmployeeModel.find_by_name(name)
        if employee:
            employee.delete_from_db()
            return {"message": "Employee deleted."}
        else:
            logging.error("Employee not found.")
        return {"message": "Employee not found."}, 404
    
class UpdateEmployee(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "employee", type=str, required=True, help="This field cannot be left blank!"
    )
    @jwt_required(optional=True)
    def put(self, id):
        data = self.parser.parse_args()

        employee = HiredEmployeeModel.find_by_id(id)

        if employee:
            employee.employee = data["employee"]
            employee.save_to_db()
        else:
            logging.error("Employee doesn't exist")
            return {"message": "Employee doesn't exist"}


        return employee.json()


class EmployeeList(Resource):
    @jwt_required(optional=True)
    def get(self):
        user_id = get_jwt_identity()
        employees = [employee.json() for employee in HiredEmployeeModel.find_all()]
        if user_id:
            return {"employees": [{"id": employee["id"],"employee": employee["name"], "datetime": employee["datetime"], "department": employee["department"], "job": employee["job"]} for employee in employees]}, 200
        else:
            return {
            "message": "More data available if you log in.",
        }, 400