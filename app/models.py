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
        DB.String(100), primary_key=True)  # Auto-incrementing
    priceTarget = DB.Column(DB.Integer, nullable=False, default=0)

    def __repr__(self):
        return f'<Signal {self.cryptoType} {self.priceTarget}>'
