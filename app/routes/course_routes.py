from flask import Blueprint

from app.controllers import course_controller as ctrl

course_bp = Blueprint("courses", __name__, url_prefix="/api/courses")


@course_bp.route("", methods=["POST"])
def create_course():
    return ctrl.create_course()


@course_bp.route("", methods=["GET"])
def get_courses():
    return ctrl.get_courses()


@course_bp.route("/<int:course_id>", methods=["GET"])
def get_course(course_id):
    return ctrl.get_course(course_id)


@course_bp.route("/<int:course_id>", methods=["PUT"])
def update_course(course_id):
    return ctrl.update_course(course_id)


@course_bp.route("/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):
    return ctrl.delete_course(course_id)
