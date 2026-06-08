import re

from flask import jsonify, request

from app.extensions import db
from app.models.lecturer_model import Lecturer

_EMAIL_RE = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')
_NAME_RE = re.compile(r'^[A-Za-z]+$')


def _validate_lecturer_payload(data, lecturer_id=None):
    errors = []
    if not data:
        return ["Request body is required."]

    first_name = str(data.get("first_name", "")).strip()
    if not first_name or not _NAME_RE.match(first_name):
        errors.append("Lecturer first name is required and must contain only letters.")

    last_name = str(data.get("last_name", "")).strip()
    if not last_name or not _NAME_RE.match(last_name):
        errors.append("Lecturer last name is required and must contain only letters.")

    email = str(data.get("email", "")).strip()
    if not _EMAIL_RE.match(email):
        errors.append("Invalid lecturer email address.")
    elif email:
        q = Lecturer.query.filter(Lecturer.email == email)
        if lecturer_id:
            q = q.filter(Lecturer.lecturer_id != lecturer_id)
        if q.first():
            errors.append("Email address already exists.")

    department = str(data.get("department", "")).strip()
    if not department:
        errors.append("Department is required.")

    return errors


def create_lecturer():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body is required."}), 400

    errors = _validate_lecturer_payload(data)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        lecturer = Lecturer(
            first_name=str(data["first_name"]).strip(),
            last_name=str(data["last_name"]).strip(),
            email=str(data["email"]).strip(),
            department=str(data["department"]).strip(),
        )
        db.session.add(lecturer)
        db.session.commit()
        return jsonify({"message": "Lecturer created successfully.", "lecturer": lecturer.to_dict()}), 201
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500


def get_lecturers():
    lecturers = Lecturer.query.all()
    return jsonify({"lecturers": [l.to_dict() for l in lecturers]}), 200


def get_lecturer(lecturer_id):
    lecturer = Lecturer.query.get(lecturer_id)
    if not lecturer:
        return jsonify({"error": "Lecturer not found."}), 404
    return jsonify({"lecturer": lecturer.to_dict()}), 200


def update_lecturer(lecturer_id):
    lecturer = Lecturer.query.get(lecturer_id)
    if not lecturer:
        return jsonify({"error": "Lecturer not found."}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No data provided to update."}), 400

    errors = _validate_lecturer_payload(data, lecturer_id=lecturer_id)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        lecturer.first_name = str(data["first_name"]).strip()
        lecturer.last_name = str(data["last_name"]).strip()
        lecturer.email = str(data["email"]).strip()
        lecturer.department = str(data["department"]).strip()
        db.session.commit()
        return jsonify({"message": "Lecturer updated successfully.", "lecturer": lecturer.to_dict()}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500


def delete_lecturer(lecturer_id):
    lecturer = Lecturer.query.get(lecturer_id)
    if not lecturer:
        return jsonify({"error": "Lecturer not found."}), 404
    try:
        db.session.delete(lecturer)
        db.session.commit()
        return jsonify({"message": "Lecturer deleted successfully."}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500
