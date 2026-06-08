from flask import jsonify, request

from app.extensions import db
from app.models.course_model import Course


def _validate_course_payload(data, course_id=None):
    errors = []
    if not data:
        return ["Request body is required."]

    course_code = str(data.get("course_code", "")).strip()
    if not course_code:
        errors.append("course_code is required.")
    elif len(course_code) > 20:
        errors.append("course_code must not exceed 20 characters.")
    else:
        q = Course.query.filter(Course.course_code == course_code)
        if course_id:
            q = q.filter(Course.course_id != course_id)
        if q.first():
            errors.append("Course code already exists.")

    course_name = str(data.get("course_name", "")).strip()
    if len(course_name) < 3:
        errors.append("Course name must be at least 3 characters.")

    credits = data.get("credits")
    if credits is None:
        errors.append("credits is required.")
    else:
        try:
            c = int(credits)
            if c < 1 or c > 6:
                errors.append("Credits must be between 1 and 6.")
        except (TypeError, ValueError):
            errors.append("Credits must be between 1 and 6.")

    lecturer_id = data.get("lecturer_id")
    if lecturer_id is None:
        errors.append("lecturer_id is required.")
    else:
        try:
            lid = int(lecturer_id)
            from app.models.lecturer_model import Lecturer
            if not Lecturer.query.get(lid):
                errors.append("Invalid lecturer selected.")
        except (TypeError, ValueError):
            errors.append("Invalid lecturer selected.")

    return errors


def create_course():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Request body is required."}), 400

    errors = _validate_course_payload(data)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        course = Course(
            course_code=str(data["course_code"]).strip(),
            course_name=str(data["course_name"]).strip(),
            credits=int(data["credits"]),
            lecturer_id=int(data["lecturer_id"]),
        )
        db.session.add(course)
        db.session.commit()
        return jsonify({"message": "Course created successfully.", "course": course.to_dict()}), 201
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500


def get_courses():
    courses = Course.query.all()
    return jsonify({"courses": [c.to_dict() for c in courses]}), 200


def get_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({"error": "Course not found."}), 404
    return jsonify({"course": course.to_dict()}), 200


def update_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({"error": "Course not found."}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No data provided to update."}), 400

    errors = _validate_course_payload(data, course_id=course_id)
    if errors:
        return jsonify({"errors": errors}), 400

    try:
        course.course_code = str(data["course_code"]).strip()
        course.course_name = str(data["course_name"]).strip()
        course.credits = int(data["credits"])
        course.lecturer_id = int(data["lecturer_id"])
        db.session.commit()
        return jsonify({"message": "Course updated successfully.", "course": course.to_dict()}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500


def delete_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({"error": "Course not found."}), 404
    try:
        db.session.delete(course)
        db.session.commit()
        return jsonify({"message": "Course deleted successfully."}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "An internal server error occurred."}), 500
