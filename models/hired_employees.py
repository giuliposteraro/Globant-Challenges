from db import db

class HiredEmployeeModel(db.Model):
    __tablename__ = "hired_employee"

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    datetime = db.Column(db.String(80))
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"), nullable=True)
    department = db.relationship("DepartmentsModel", back_populates="hired_employee")
    jobs_id = db.Column(db.Integer, db.ForeignKey("jobs.id"), nullable=True)
    job = db.relationship("JobsModel", back_populates="hired_employee")

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "datetime": self.datetime,
            "department": self.department_id,
            "job": self.jobs_id
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
    
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