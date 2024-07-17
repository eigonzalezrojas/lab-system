from src import db

class Invoice(db.Model):
    __tablename__ = 'invoices'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    user_first_name = db.Column(db.String(64), nullable=False)
    user_last_name = db.Column(db.String(64), nullable=False)
    user_rut = db.Column(db.String(12), db.ForeignKey('user_accounts.rut'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Float, nullable=False)

    user = db.relationship('UserAccount', backref=db.backref('invoices', lazy=True))

    def __repr__(self):
        return f'<Invoice {self.id}>'