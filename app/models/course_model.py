from app.extensions import db


class Course(db.Model):
    __tablename__ = "courses"

    course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_code = db.Column(db.String(20), nullable=False, unique=True)
    course_name = db.Column(db.String(100), nullable=False)
    credits = db.Column(db.Integer, nullable=False)
    lecturer_id = db.Column(db.Integer, db.ForeignKey("lecturers.lecturer_id"), nullable=False)

    def to_dict(self):
        return {
            "course_id": self.course_id,
            "course_code": self.course_code,
            "course_name": self.course_name,
            "credits": self.credits,
            "lecturer_id": self.lecturer_id,
        }
