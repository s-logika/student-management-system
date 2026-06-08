from flask import Blueprint

from app.controllers import lecturer_controller as ctrl

lecturer_bp = Blueprint("lecturers", __name__, url_prefix="/api/lecturers")


@lecturer_bp.route("", methods=["POST"])
def create_lecturer():
    return ctrl.create_lecturer()


@lecturer_bp.route("", methods=["GET"])
def get_lecturers():
    return ctrl.get_lecturers()


@lecturer_bp.route("/<int:lecturer_id>", methods=["GET"])
def get_lecturer(lecturer_id):
    return ctrl.get_lecturer(lecturer_id)


@lecturer_bp.route("/<int:lecturer_id>", methods=["PUT"])
def update_lecturer(lecturer_id):
    return ctrl.update_lecturer(lecturer_id)


@lecturer_bp.route("/<int:lecturer_id>", methods=["DELETE"])
def delete_lecturer(lecturer_id):
    return ctrl.delete_lecturer(lecturer_id)
