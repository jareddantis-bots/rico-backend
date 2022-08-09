from database import db


class Session(db.Model):
    __tablename__ = 'sessions'
    id = db.Column(db.String, primary_key=True, nullable=False)
    state = db.Column(db.String, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=True)

    user = db.relationship('User', backref='sessions', lazy=True)

    def __repr__(self):
        return f'<Session user_id={self.user_id} session_id={self.session_id}>'
