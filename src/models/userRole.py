from src import db

class UserRole(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    users = db.relationship('UserAccount', backref='role', lazy=True)

    def __repr__(self):
        return f'<UserRole {self.name}>'
