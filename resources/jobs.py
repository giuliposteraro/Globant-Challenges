from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt
from sqlalchemy.exc import SQLAlchemyError
from models import JobsModel
import logging

logging.basicConfig(filename='LOGS/api.log', level=logging.ERROR, format="%(asctime)s %(levelname)s %(message)s")

class Job(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "job", type=str, required=True, help="This field cannot be left blank!"
    )

    @jwt_required()
    def get(self, job):
        job = JobsModel.find_by_name(job)
        if job:
            return job.json()
        else:
            logging.error("Job not found")
        return {"message": "Job not found"}, 404

    @jwt_required(fresh=True)
    def post(self, job):
        if JobsModel.find_by_name(job):
            logging.error("A job with name '{}' already exists.".format(job))
            return {
                "message": "A job with name '{}' already exists.".format(job)
            }, 400

        data = self.parser.parse_args()

        job = JobsModel(**data)

        try:
            job.save_to_db()
        except SQLAlchemyError as e:
            logging.error(str(e))
            return {"message": "An error occurred while inserting the item."}, 500

        return job.json(), 201

    @jwt_required()
    def delete(self, job):
        # jwt = get_jwt()
        # if not jwt["is_admin"]:
        #     return {"message": "Admin privilege required."}, 401

        job = JobsModel.find_by_name(job)
        if job:
            job.delete_from_db()
            return {"message": "Job deleted."}
        else:
            logging.error("Job not found")
        return {"message": "Job not found."}, 404

class UpdateJob(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "job", type=str, required=True, help="This field cannot be left blank!"
    )
    @jwt_required(optional=True)
    def put(self, id):
        data = self.parser.parse_args()

        job = JobsModel.find_by_id(id)

        if job:
            job.job = data["job"]
            job.save_to_db()
        else:
            logging.error("Job doesn't exist")
            return {"message": "Job doesn't exist"}

        return job.json()


class JobList(Resource):
    @jwt_required(optional=True)
    def get(self):
        user_id = get_jwt_identity()
        jobs = [job.json() for job in JobsModel.find_all()]
        if user_id:
            return {"jobs": [{"id": job["id"],"job": job["job"]} for job in jobs]}, 200
        else:
            return {
            "message": "More data available if you log in.",
        }, 400