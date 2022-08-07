from database import db
from datetime import datetime
from flask import jsonify, request
from models.guild import Guild, GuildNote
from models.user import User, UserNote
from uuid6 import uuid7


def create_note():
    # Check request body
    try:
        for_guild = request.json['for_guild']
        sender_details = request.json['sender']
        recipient_details = request.json['recipient']
        sender_id = sender_details['id']
        recipient_id = recipient_details['id']
        note_type = request.json['type']
        title = request.json['title']

        # Optional args
        url = request.json.get('url', '')
        sender_name = sender_details.get('name', '')
        sender_discriminator = sender_details.get('discriminator', '')
        recipient_name = recipient_details.get('name', '')
        recipient_discriminator = recipient_details.get('discriminator', '')
    except KeyError as e:
        return {
            'success': False,
            'error': f'Missing key in request body: {e}'
        }, 400

    # Check if the sender exists in the user database
    sender = User.query.get(sender_id)
    if sender is None:
        if not sender_name or not sender_discriminator:
            return {
                'success': False,
                'error': 'Sender does not exist in database, and their given details are incomplete'
            }, 400

        # Add user to database
        sender = User(
            id=sender_id,
            username=sender_name,
            discriminator=sender_discriminator
        )
        db.session.add(sender)
        db.session.commit()

    # Check if the recipient exists in the database
    if for_guild:
        recipient = Guild.query.get(recipient_id)
        if recipient is None:
            if not recipient_name:
                return {
                    'success': False,
                    'error': 'Guild does not exist in database, and the given details are incomplete'
                }, 400

            # Add guild to database
            recipient = Guild(
                id=recipient_id,
                name=recipient_name
            )
            db.session.add(recipient)
            db.session.commit()

        note = GuildNote(
            id=str(uuid7()),
            timestamp=datetime.now(),
            sender=sender_id,
            recipient=recipient_id,
            type=note_type,
            title=title,
            url=url
        )
    else:
        # Don't check recipient if this is a note to self
        if sender_id != recipient_id:
            recipient = User.query.get(recipient_id)
            if recipient is None:
                if not recipient_name or not recipient_discriminator:
                    return {
                       'success': False,
                       'error': 'Receiver does not exist in database, and their given details are incomplete'
                    }, 400

                # Add user to database
                recipient = User(
                    id=recipient_id,
                    username=recipient_name,
                    discriminator=recipient_discriminator
                )
                db.session.add(recipient)
                db.session.commit()

        note = UserNote(
            id=str(uuid7()),
            timestamp=datetime.now(),
            sender=sender_id,
            recipient=recipient_id,
            type=note_type,
            title=title,
            url=url
        )

    # Add note to database
    db.session.add(note)
    db.session.commit()

    # Return ID
    return {
        'success': True,
        'note_id': note.id
    }, 200


def get_notes():
    # Check request body
    try:
        is_guild = request.json['guild']
        owner = request.json['owner']
    except KeyError as e:
        return {
            'success': False,
            'error': f'Missing key in request body: {e}'
        }, 400

    # Fetch all notes
    if is_guild:
        notes = GuildNote.query.filter_by(recipient=owner).order_by(GuildNote.timestamp).all()
    else:
        notes = UserNote.query.filter_by(recipient=owner).order_by(UserNote.timestamp).all()

    # Return notes
    return jsonify([{
        'id': x.id,
        'timestamp': x.timestamp.timestamp(),
        'sender': x.sender,
        'recipient': x.recipient,
        'type': x.type,
        'title': x.title,
        'url': x.url
    } for x in notes])
