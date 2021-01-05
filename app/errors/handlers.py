from app.errors import bp
from flask import render_template
from werkzeug.exceptions import InternalServerError


@bp.app_errorhandler(404)
def pageNotFound(e):
    return render_template('errors/404.html'), 404


@bp.app_errorhandler(500)
def internalServerError(e: InternalServerError):
    return render_template('errors/500.html'), 500
