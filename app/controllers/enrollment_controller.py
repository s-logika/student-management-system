from datetime import datetime

from flask import jsonify, request

from app.extensions import db
from app.models.enrollment_model import Enrollment

_VALID_STATUSES = {"Active", "Completed", "Dropped"}


def _parse_date(value):
    try:
        return datetime.strptime(str(value).strip(), "%Y-%m-%d").date(), None
    except ValueError:
        return None, "Date must be in YYYY-MM-DD format."


def _validate_enrollment_payload(data, enrollment_id=None):
    errors = []
    if not data:
        return ["Request body is required."]

    student_id = data.get("student_id")
    if student_id is None:
        errors.append("student_id is required.")
    else:
        try:
            sid = int(student_id)
            from app.models.student_model import Student
            if not Student.query.get(sid):
                errors.append("Invalid student selected.")
        except (TypeError, ValueError):
            errors.append("Invalid student selected.")

    course_id = data.get("course_id")
    if course_id is None:
        errors.append("course_id is required.")
    else:
        try:
            cid = int(course_id)
            from app.models.course_model import Course
            if not Course.query.get(cid):
                errors.append("Invalid course selected.")
        except (TypeError, ValueError):
            errors.append("Invalid course selected.")

    enrollment_date_raw = data.get("enrollment_date")
    if not enrollment_date_raw:
        errors.append("Enrollment date is required.")
    else:
        _, err = _parse_date(enrollment_date_raw)
        if err:
            errors.append(err)

    status = str(data.get("status", "")).strip()
    if status not in _VALID_STATUSES:
        errors.append("Invalid enrollment status. Must be Active, Completed, or Dropped.")

    return errors


def create_enrollment():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body is required."}), 400

    errors = _validate_enrollment_payload(data)
    if errors:
        return jsonify({"errors": errors}), 400

    enrollment_date, _ = _parse_date(data.get("enrollment_date"))
    try:
        enrollment = Enrollment(
            student_id=int(data["student_id"]),
            course_id=int(data["course_id"]),
            enrollment_date=enrollment_date,
            status=str(data["status"]).strip(),
        )
        db.session.add(enrollment)
        db.session.commit()
        return jsonify({"message": "Enrollment created successfully.", "enrollment": enrollment.to_dict()}), 201
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500


def get_enrollments():
    enrollments = Enrollment.query.all()
    return jsonify({"enrollments": [e.to_dict() for e in enrollments]}), 200


def get_enrollment(enrollment_id):
    enrollment = Enrollment.query.get(enrollment_id)
    if not enrollment:
        return jsonify({"error": "Enrollment not found."}), 404
    return jsonify({"enrollment": enrollment.to_dict()}), 200


def update_enrollment(enrollment_id):
    enrollment = Enrollment.query.get(enrollment_id)
    if not enrollment:
        return jsonify({"error": "Enrollment not found."}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No data provided to update."}), 400

    errors = _validate_enrollment_payload(data, enrollment_id=enrollment_id)
    if errors:
        return jsonify({"errors": errors}), 400

    enrollment_date, _ = _parse_date(data.get("enrollment_date"))
    try:
        enrollment.student_id = int(data["student_id"])
        enrollment.course_id = int(data["course_id"])
        enrollment.enrollment_date = enrollment_date
        enrollment.status = str(data["status"]).strip()
        db.session.commit()
        return jsonify({"message": "Enrollment updated successfully.", "enrollment": enrollment.to_dict()}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500


def delete_enrollment(enrollment_id):
    enrollment = Enrollment.query.get(enrollment_id)
    if not enrollment:
        return jsonify({"error": "Enrollment not found."}), 404
    try:
        db.session.delete(enrollment)
        db.session.commit()
        return jsonify({"message": "Enrollment deleted successfully."}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500
