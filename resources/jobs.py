from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError
from models import JobsModel


class Job(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "job", type=str, required=True, help="This field cannot be left blank!"
    )

    @jwt_required()
    def get(self, name):
        job = JobsModel.find_by_name(name)
        if job:
            return job.json()
        return {"message": "Job not found"}, 404

    @jwt_required(fresh=True)
    def post(self, name):
        if JobsModel.find_by_name(name):
            return {
                "message": "A job with name '{}' already exists.".format(name)
            }, 400

        data = self.parser.parse_args()

        job = JobsModel(name=name, **data)

        try:
            job.save_to_db()
        except SQLAlchemyError:
            return {"message": "An error occurred while inserting the item."}, 500

        return job.json(), 201

    @jwt_required()
    def delete(self, name):
        jwt = get_jwt()
        if not jwt["is_admin"]:
            return {"message": "Admin privilege required."}, 401

        job = JobsModel.find_by_name(name)
        if job:
            job.delete_from_db()
            return {"message": "Job deleted."}
        return {"message": "Job not found."}, 404

    def put(self, name):
        data = self.parser.parse_args()

        job = JobsModel.find_by_name(name)

        if job:
            job.job = data["job"]
        else:
            job = JobsModel(name, **data)

        job.save_to_db()

        return job.json()


class JobList(Resource):
    @jwt_required(optional=True)
    def get(self):
        user_id = get_jwt_identity()
        jobs = [job.json() for job in JobsModel.find_all()]
        if user_id:
            return {"items": jobs}, 200
        return {
            "jobs": [job["name"] for job in jobs],
            "message": "More data available if you log in.",
        }, 200