from flask import Blueprint

from app.controllers import enrollment_controller as ctrl

enrollment_bp = Blueprint("enrollments", __name__, url_prefix="/api/enrollments")


@enrollment_bp.route("", methods=["POST"])
def create_enrollment():
    return ctrl.create_enrollment()


@enrollment_bp.route("", methods=["GET"])
def get_enrollments():
    return ctrl.get_enrollments()


@enrollment_bp.route("/<int:enrollment_id>", methods=["GET"])
def get_enrollment(enrollment_id):
    return ctrl.get_enrollment(enrollment_id)


@enrollment_bp.route("/<int:enrollment_id>", methods=["PUT"])
def update_enrollment(enrollment_id):
    return ctrl.update_enrollment(enrollment_id)


@enrollment_bp.route("/<int:enrollment_id>", methods=["DELETE"])
def delete_enrollment(enrollment_id):
    return ctrl.delete_enrollment(enrollment_id)
