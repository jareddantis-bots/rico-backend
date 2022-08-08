from database import db
from flask import request
from middleware.auth import login_required
from models.guild import Guild, ExcludedThread


@login_required
def add_excluded_thread():
    # Check request body
    try:
        guild_id = request.json['guild_id']
        thread_id = request.json['thread_id']

        if not isinstance(guild_id, int):
            raise ValueError('guild_id must be an integer')
        if not isinstance(thread_id, int):
            raise ValueError('thread_id must be an integer')
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
        return {
            'success': False,
            'error': f'Guild {guild_id} does not exist'
        }, 404
    else:
        # Check if thread monitoring is enabled
        if not guild.manage_threads:
            return {
                'success': False,
                'error': f'Thread monitoring is not enabled for guild {guild_id}'
            }, 404

    # Check if thread is already in DB
    excluded_thread = ExcludedThread.query.filter_by(guild_id=guild_id, thread_id=thread_id).first()
    if excluded_thread is not None:
        return {
            'success': False,
            'error': f'Thread {thread_id} in guild {guild_id} is already excluded'
        }, 409

    # Create excluded thread
    excluded_thread = ExcludedThread(
        thread_id=thread_id,
        guild_id=guild_id
    )

    # Add to database
    db.session.add(excluded_thread)
    db.session.commit()
    return {
        'success': True
    }, 200


@login_required
def delete_excluded_thread():
    # Check request body
    try:
        guild_id = request.json['guild_id']
        thread_id = request.json['thread_id']

        if not isinstance(guild_id, int):
            raise ValueError('guild_id must be an integer')
        if not isinstance(thread_id, int):
            raise ValueError('thread_id must be an integer')
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
        return {
            'success': False,
            'error': f'Guild {guild_id} does not exist'
        }, 404
    else:
        # Check if thread monitoring is enabled
        if not guild.manage_threads:
            return {
                'success': False,
                'error': f'Thread monitoring is not enabled for guild {guild_id}'
            }, 404

    # Check if thread is already in DB
    excluded_thread = ExcludedThread.query.filter_by(guild_id=guild_id, thread_id=thread_id).first()
    if excluded_thread is None:
        return {
            'success': False,
            'error': f'Thread {thread_id} in guild {guild_id} is not excluded'
        }, 404

    # Delete excluded thread
    db.session.delete(excluded_thread)
    db.session.commit()
    return {
        'success': True
    }, 200


@login_required
def get_excluded_threads():
    # Check request body
    try:
        guild_id = request.json['guild_id']

        if not isinstance(guild_id, int):
            raise ValueError('guild_id must be an integer')
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
        return {
            'success': False,
            'error': f'Guild {guild_id} does not exist'
        }, 404
    else:
        # Check if thread monitoring is enabled
        if not guild.manage_threads:
            return {
                'success': False,
                'error': f'Thread monitoring is not enabled for guild {guild_id}'
            }, 404

    # Return excluded threads
    excluded_threads = ExcludedThread.query.filter_by(guild_id=guild_id).all()
    return {
        'success': True,
        'excluded_threads': [excluded_thread.thread_id for excluded_thread in excluded_threads]
    }, 200
