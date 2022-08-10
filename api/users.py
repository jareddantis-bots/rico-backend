from database import db
from datetime import datetime
from flask import request
from middleware.auth import login_required, admin_only, user_only
from models.user import User


@admin_only
def update_user():
    # Check request body
    try:
        user_id = request.json['id']
        user_name = request.json['name']
        user_discriminator = request.json['discriminator']

        if not isinstance(user_id, int):
            raise ValueError('id must be an integer')
        if not user_name or len(user_name) > 255:
            raise ValueError('name must be between 0 to 256 characters long')
        if not user_discriminator or len(user_discriminator) > 255:
            raise ValueError('discriminator must be between 0 to 256 characters long')
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

    # Check if user is already in DB
    user = User.query.get(user_id)
    if user is None:
        # Create user
        user = User(
            id=user_id,
            username=user_name,
            discriminator=user_discriminator
        )

        # Add to DB
        db.session.add(user)
    else:
        # Update existing user
        user.name = user_name
        user.discriminator = user_discriminator

    # Commit
    db.session.commit()
    return {
        'success': True
    }, 200


@login_required
def delete_user():
    # Check request body
    try:
        user_id = request.json['id']

        if not isinstance(user_id, int):
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

    # Check if user is in DB
    user = User.query.get(user_id)
    if user is not None:
        # Delete user
        db.session.delete(user)
        db.session.commit()

    return {
        'success': True
    }, 200


@user_only
def update_user_spotify_credentials():
    # Check request body
    try:
        user_id = request.json['id']
        access_token = request.json['access_token']
        refresh_token = request.json['refresh_token']
        expires_at = request.json['expires_at']

        if not isinstance(user_id, int):
            raise ValueError('id must be an integer')
        if not isinstance(expires_at, float):
            raise ValueError('expires_at must be a timestamp expressed as a floating-point number')
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

    # Get user
    user = User.query.get(user_id)
    if user is None:
        return {
            'success': False,
            'error': f'User {user_id} does not exist'
        }, 404

    # Update user credentials
    user.spotify_access_token = access_token
    user.spotify_refresh_token = refresh_token
    user.spotify_expires_at = datetime.fromtimestamp(expires_at)

    # Save to database
    db.session.commit()
    return {
        'success': True
    }
