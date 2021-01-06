from app.home import bp
from enums import ServerCode
from flask import render_template


@bp.route('/')
def home():
    return render_template('home/home.html'), ServerCode.OK
