from app.home import bp
from enums import ServerCode, ServerStatus
from flask import render_template, jsonify


@bp.route('/admin')
def home():
    return render_template('admin/home.html'), ServerCode.OK
