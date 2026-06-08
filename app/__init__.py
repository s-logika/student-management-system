from flask import Flask, jsonify

from app.config import Config
from app.extensions import db
from app.routes import register_blueprints
from sqlalchemy.exc import OperationalError, ProgrammingError


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    from app.models import Course, Enrollment, Lecturer, Student  # noqa: F401

    register_blueprints(app)

    @app.errorhandler(OperationalError)
    def handle_operational_error(err):
        db.session.rollback()
        orig = getattr(err, "orig", None)
        code = orig.args[0] if orig and orig.args else None
        if code == 1049:
            return jsonify({"error": "Invalid database name configured."}), 500
        if code in (2003, 2002):
            return jsonify({"error": "MySQL server is not running or not reachable."}), 503
        return jsonify({"error": "Database connection failed."}), 500

    @app.errorhandler(ProgrammingError)
    def handle_programming_error(err):
        db.session.rollback()
        return jsonify({"error": "Invalid database name configured."}), 500

    @app.errorhandler(500)
    def handle_internal_error(err):
        return jsonify({"error": "An internal server error occurred."}), 500

    return app
