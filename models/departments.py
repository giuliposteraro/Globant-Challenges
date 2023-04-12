from db import db
class DepartmentsModel(db.Model):
    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    hired_employee = db.relationship("HiredEmployeeModel")

    def json(self):
        return {
            "id": self.id,
            "name": self.name
        }

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
