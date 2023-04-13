from db import db

class JobsModel(db.Model):
    __tablename__ = "jobs"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    job = db.Column(db.String(80), nullable=False)
    hired_employee = db.relationship("HiredEmployeeModel")

    def json(self):
        return {
            "id": self.id,
            "job": self.job
        }

    @classmethod
    def find_by_name(cls, job):
        return cls.query.filter_by(job=job).first()
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
