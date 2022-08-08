from database import db
from flask import request
from middleware.auth import login_required
from models.guild import Guild
from typing import Dict, Optional, Tuple


def check_request(req: request, id_only: Optional[bool] = False) -> int | Tuple[int, str, bool] | Tuple[Dict[str, str], int]:
    # Check request body
    guild_name = ''
    guild_manage_threads = False
    try:
        guild_id = req.json['id']

        if not isinstance(guild_id, int):
            raise ValueError('id must be an integer')

        if not id_only:
            guild_name = req.json.get('name', guild_name)
            guild_manage_threads = req.json.get('manage_threads', guild_manage_threads)

            if 'name' in req.json and not isinstance(guild_name, str):
                raise ValueError('name must be a string')
            if 'name' in req.json and not 0 < len(guild_name) < 256:
                raise ValueError('name must be between 0 to 256 characters long')
            if 'manage_threads' in req.json and not isinstance(guild_manage_threads, bool):
                raise ValueError('manage_threads must be a boolean')
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
    else:
        return guild_id if id_only else guild_id, guild_name, guild_manage_threads


@login_required
def add_guild():
    # Check request body
    check_result = check_request(request)
    if isinstance(check_result[0], dict):
        return check_result
    guild_id, guild_name, guild_manage_threads = check_result

    # Check if guild is already in DB
    guild = Guild.query.get(guild_id)
    if guild is not None:
        return {
            'success': False,
            'error': 'Guild already exists'
        }, 409

    # Create guild
    guild = Guild(
        id=guild_id,
        name=guild_name,
        manage_threads=guild_manage_threads
    )

    # Add to DB
    db.session.add(guild)
    db.session.commit()
    return {
        'success': True
    }


@login_required
def update_guild():
    # Check request body
    check_result = check_request(request)
    if isinstance(check_result[0], dict):
        return check_result
    guild_id, guild_name, guild_manage_threads = check_result

    # Check if guild is already in DB
    guild = Guild.query.get(guild_id)
    if guild is None:
        return {
            'success': False,
            'error': f'Guild {guild_id} does not exist'
        }, 404

    # Update existing guild
    if 'name' in request.json:
        guild.name = guild_name
    if 'manage_threads' in request.json:
        guild.manage_threads = guild_manage_threads

    # Commit
    db.session.commit()


@login_required
def delete_guild():
    # Check request body
    check_result = check_request(request, id_only=True)
    if isinstance(check_result, tuple) and isinstance(check_result[0], dict):
        return check_result
    guild_id = check_result

    # Check if guild is in DB
    guild = Guild.query.get(guild_id)
    if guild is not None:
        # Delete user
        db.session.delete(guild)
        db.session.commit()

    return {
        'success': True
    }, 200


@login_required
def get_guild():
    # Check request body
    check_result = check_request(request, id_only=True)
    if isinstance(check_result, tuple) and isinstance(check_result[0], dict):
        return check_result
    guild_id = check_result

    # Check if guild is in DB
    guild = Guild.query.get(guild_id)
    if guild is None:
        return {
            'success': False,
            'error': 'Guild not found'
        }, 404

    # Return guild data
    return {
        'success': True,
        'guild': {
            'name': guild.name,
            'manage_threads': guild.manage_threads
        }
    }, 200
