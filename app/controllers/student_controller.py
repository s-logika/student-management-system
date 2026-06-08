import re
from datetime import date, datetime

from flask import jsonify, request

from app.extensions import db
from app.models.student_model import Student

_EMAIL_RE = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')
_NAME_RE = re.compile(r'^[A-Za-z]{2,50}$')


def _parse_date(value):
    try:
        return datetime.strptime(str(value).strip(), "%Y-%m-%d").date(), None
    except ValueError:
        return None, "Date must be in YYYY-MM-DD format."


def _validate_student_payload(data, student_id=None):
    errors = []
    if not data:
        return ["Request body is required."]

    first_name = str(data.get("first_name", "")).strip()
    if not _NAME_RE.match(first_name):
        errors.append("First name must contain only letters (2-50 characters).")

    last_name = str(data.get("last_name", "")).strip()
    if not _NAME_RE.match(last_name):
        errors.append("Last name must contain only letters (2-50 characters).")

    email = str(data.get("email", "")).strip()
    if not _EMAIL_RE.match(email):
        errors.append("Please enter a valid email address.")
    elif email:
        q = Student.query.filter(Student.email == email)
        if student_id:
            q = q.filter(Student.student_id != student_id)
        if q.first():
            errors.append("Email address already exists.")

    dob_raw = data.get("date_of_birth")
    if not dob_raw:
        errors.append("date_of_birth is required.")
    else:
        dob, err = _parse_date(dob_raw)
        if err:
            errors.append(err)
        elif dob >= date.today():
            errors.append("Date of birth cannot be a future date.")

    return errors


def create_student():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body is required."}), 400

    errors = _validate_student_payload(data)
    if errors:
        return jsonify({"errors": errors}), 400

    dob, _ = _parse_date(data.get("date_of_birth"))
    try:
        student = Student(
            first_name=str(data["first_name"]).strip(),
            last_name=str(data["last_name"]).strip(),
            email=str(data["email"]).strip(),
            date_of_birth=dob,
        )
        db.session.add(student)
        db.session.commit()
        return jsonify({"message": "Student created successfully.", "student": student.to_dict()}), 201
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500


def get_students():
    students = Student.query.all()
    return jsonify({"students": [s.to_dict() for s in students]}), 200


def get_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"error": "Student not found."}), 404
    return jsonify({"student": student.to_dict()}), 200


def update_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"error": "Student not found."}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No data provided to update."}), 400

    errors = _validate_student_payload(data, student_id=student_id)
    if errors:
        return jsonify({"errors": errors}), 400

    dob, _ = _parse_date(data.get("date_of_birth"))
    try:
        student.first_name = str(data["first_name"]).strip()
        student.last_name = str(data["last_name"]).strip()
        student.email = str(data["email"]).strip()
        student.date_of_birth = dob
        db.session.commit()
        return jsonify({"message": "Student updated successfully.", "student": student.to_dict()}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500


def delete_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"error": "Student not found."}), 404
    try:
        db.session.delete(student)
        db.session.commit()
        return jsonify({"message": "Student deleted successfully."}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500
