from database import db


class DiscordOAuth2(db.Model):
    __tablename__ = 'discord_oauth2'
    user_id = db.Column(db.BigInteger, db.ForeignKey('users.id'),  primary_key=True, nullable=False)
    access_token = db.Column(db.String, nullable=False)
    refresh_token = db.Column(db.String, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    session_id = db.Column(db.String, db.ForeignKey('sessions.id'), nullable=True)

    session = db.relationship('Session', backref='discord_oauth2', lazy=True)
    user = db.relationship('User', backref='discord_oauth2', lazy=True)

    def __repr__(self):
        return f'<DiscordOAuth2 user_id={self.user_id}>'
