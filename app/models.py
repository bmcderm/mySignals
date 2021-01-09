from app import DB

"""
DATABASE COMMANDS
flask db init
flask db migrate -m "Initial"
flask db upgrade
"""


class Signal(DB.Model):
    __tablename__ = 'signal'
    cryptoType = DB.Column(
        DB.String(100), primary_key=True)
    postDate = DB.Column(DB.Integer, primary_key=True)
    priceTarget = DB.Column(DB.Integer, nullable=False, default=0)
    notes = DB.Column(DB.String(300), nullable=True)
    accumulateRange = DB.Column(DB.String(300), nullable=False)
    sellingTargets = DB.Column(DB.String(300), nullable=False)
    stopLoss = DB.Column(DB.Float, nullable=False, default=0)
    entryZone = DB.Column(DB.String(300), nullable=False)
    currentAsk = DB.Column(DB.Float, nullable=False)
    target1 = DB.Column(DB.Float, nullable=False)
    target2 = DB.Column(DB.Float, nullable=False)
    target3 = DB.Column(DB.Float, nullable=False)

    volume = DB.Column(DB.String(300), nullable=True)
    term = DB.Column(DB.String(20), nullable=False)
    risk = DB.Column(DB.String(20), nullable=False)

    def __repr__(self):
        return f'<Signal {self.cryptoType} {self.priceTarget}>'
