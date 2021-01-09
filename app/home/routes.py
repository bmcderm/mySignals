from app import models
from app.home import bp
from enums import ServerCode, ServerStatus
from flask import render_template, jsonify


@bp.route('/')
def home():
    return render_template('home/home.html'), ServerCode.OK


@bp.route('/getRecentSignals', methods=['GET'])
def getRecentSignals():
    signals = models.Signal.query.all()

    d = []
    for s in signals:
        d.append({
            'cryptoType': s.cryptoType,
        })

    return jsonify({
        'status': ServerStatus.OK,
        'signals': d,
    }), ServerCode.OK


@bp.route('/features')
def features():
    return 'features'
