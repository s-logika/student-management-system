from app.extensions import db


class Lecturer(db.Model):
    __tablename__ = "lecturers"

    lecturer_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    department = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            "lecturer_id": self.lecturer_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "department": self.department,
        }
