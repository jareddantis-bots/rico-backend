from database import db
from flask import request
from middleware.auth import login_required
from models.guild import Guild


@login_required
def update_guild():
    # Check request body
    try:
        guild_id = request.json['id']
        guild_name = request.json['name']

        if not isinstance(guild_id, int):
            raise ValueError('id must be an integer')
        if not guild_name or len(guild_name) > 255:
            raise ValueError('name must be between 0 to 256 characters long')
    except KeyError as e:
        return {
            'success': False,
            'error': f'Missing key in request body: {e}'
        }, 400
    except ValueError as e:
        return {
            'success': False,
            'error': f'Bad value: {e}'
        }, 400

    # Check if guild is already in DB
    guild = Guild.query.get(guild_id)
    if guild is None:
        # Create guild
        guild = Guild(
            id=guild_id,
            name=guild_name
        )

        # Add to DB
        db.session.add(guild)
    else:
        # Update existing guild
        guild.name = guild_name

    # Commit
    db.session.commit()


@login_required
def delete_guild():
    # Check request body
    try:
        guild_id = request.json['id']

        if not isinstance(guild_id, int):
            raise ValueError('id must be an integer')
    except KeyError as e:
        return {
            'success': False,
            'error': f'Missing key in request body: {e}'
        }, 400
    except ValueError as e:
        return {
            'success': False,
            'error': f'Bad value: {e}'
        }, 400

    # Check if guild is in DB
    guild = Guild.query.get(guild_id)
    if guild is not None:
        # Delete user
        db.session.delete(guild)
        db.session.commit()

    return {
        'success': True
    }, 200
