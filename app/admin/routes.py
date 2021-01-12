from app.admin import bp
from util import DiscordResponse
from enums import ServerCode, ServerStatus
from flask import render_template, jsonify
from flaskHelpers import requireAdminRole, apiRequireAdminRole


@bp.route('/admin')
@requireAdminRole
def home(discordResponse: DiscordResponse):
    return render_template('admin/home.html'), ServerCode.OK
