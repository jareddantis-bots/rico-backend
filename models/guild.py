from database import db


class Guild(db.Model):
    __tablename__ = 'guilds'
    id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    manage_threads = db.Column(db.Boolean, default=False)
    excluded_threads = db.relationship('ExcludedThread', cascade='all, delete-orphan', backref='guild', lazy=True)
    inbox = db.relationship('GuildNote', cascade='all, delete-orphan', backref='recipient_guild', lazy=True)

    def __repr__(self):
        return f'<Guild name="{self.name}" id={self.id}>'


class ExcludedThread(db.Model):
    __tablename__ = 'excl_threads'
    thread_id = db.Column(db.BigInteger, primary_key=True, nullable=False)
    guild_id = db.Column(db.BigInteger, db.ForeignKey('guilds.id'), nullable=False)

    def __repr__(self):
        return f'<Thread id="{self.thread_id}" guild="{self.guild_id}">'


class GuildNote(db.Model):
    __tablename__ = 'guild_notes'
    id = db.Column(db.String, primary_key=True, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    sender = db.Column(db.BigInteger, db.ForeignKey('users.id'), nullable=False)
    recipient = db.Column(db.BigInteger, db.ForeignKey('guilds.id'), nullable=False)
    type = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<Note for_guild=True id={self.id} title="{self.title}">'
