from database import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    username = db.Column(db.String, nullable=False)
    discriminator = db.Column(db.String, nullable=False)
    spotify_access_token = db.Column(db.String)
    spotify_refresh_token = db.Column(db.String)
    spotify_expires_at = db.Column(db.DateTime)
    inbox = db.relationship('UserNote', cascade='all, delete-orphan', backref='note_recipient',
                            lazy=True, foreign_keys='[UserNote.recipient]')

    def __repr__(self):
        return f'<User name="{self.username}#{self.discriminator}">'


class UserNote(db.Model):
    __tablename__ = 'user_notes'
    id = db.Column(db.String, primary_key=True, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    sender = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False)
    recipient = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<Note for_guild=False id={self.id} title="{self.title}">'
