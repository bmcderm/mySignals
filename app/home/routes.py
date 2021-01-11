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
            'postDate': s.postDate,
            'priceTarget': s.priceTarget,
            'notes': s.notes,
            'accumulateRange': s.accumulateRange,
            'sellingTargets': s.sellingTargets,
            'stopLoss': s.stopLoss,
            'entryZone': s.entryZone,
            'currentAsk': s.currentAsk,
            'target1': s.target1,
            'target2': s.target2,
            'target3': s.target3,
            'volume': s.volume,
            'term': s.term,
            'risk': s.risk,
        })

    return jsonify({
        'status': ServerStatus.OK,
        'signals': d,
    }), ServerCode.OK
