from database import db
from datetime import datetime
from flask import current_app, make_response, redirect, request
from models.discord_oauth2 import DiscordOAuth2
from models.session import Session
from models.user import User
from secrets import token_hex, token_urlsafe
from time import time
from urllib.parse import urlencode
import requests


def discord_oauth2_begin():
    # Create new session, valid for 1 hour
    session_id = token_hex(16)
    session = Session(
        id=session_id,
        state=token_urlsafe(16),
        expires_at=datetime.fromtimestamp(time() + 3600)
    )

    # Add session to DB
    db.session.add(session)
    db.session.commit()

    # Form URL for OAuth2 login
    base_url = 'https://discord.com/api/oauth2/authorize'
    params = {
        'client_id': current_app.config['DISCORD_CLIENT_ID'],
        'redirect_uri': current_app.config['DISCORD_CALLBACK_URI'],
        'response_type': 'code',
        'scope': ' '.join([
            'identify',
            'guilds',
        ]),
        'state': session.state,
        'prompt': 'none'
    }
    url = f'{base_url}?{urlencode(params)}'

    # Create redirect response
    response = make_response(redirect(url))
    return response


def discord_oauth2_callback():
    # Check request body
    if 'code' not in request.json:
        return 'Missing code', 400
    if 'state' not in request.json:
        return 'Missing state', 400

    # Check for state in session table
    session = Session.query.filter_by(state=request.json['state']).first()
    if session is None:
        return 'Invalid state', 400

    # Form URL for OAuth2 token exchange
    token_url = 'https://discord.com/api/oauth2/token'
    params = {
        'client_id': current_app.config['DISCORD_CLIENT_ID'],
        'client_secret': current_app.config['DISCORD_CLIENT_SECRET'],
        'grant_type': 'authorization_code',
        'code': request.json['code'],
        'redirect_uri': current_app.config['DISCORD_CALLBACK_URI']
    }

    # Exchange OAuth2 code for token
    response = requests.post(
        token_url,
        data=params,
        headers={
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    )
    if response.status_code != 200:
        db.session.delete(session)
        db.session.commit()
        return 'Could not exchange code for token', response.status_code

    # Parse token response
    token_response = response.json()
    if 'access_token' not in token_response:
        db.session.delete(session)
        db.session.commit()
        return 'Could not parse token response', 400

    # Get user details
    user_response = requests.get(
        'https://discord.com/api/oauth2/@me',
        headers={
            'Authorization': f'Bearer {token_response["access_token"]}'
        }
    )
    if user_response.status_code != 200:
        db.session.delete(session)
        db.session.commit()
        return 'Could not get user details', user_response.status_code

    # Parse user details response
    user_details = user_response.json()
    try:
        user_id = int(user_details['user']['id'])
        user_name = user_details['user']['username']
        user_discriminator = user_details['user']['discriminator']
    except KeyError:
        db.session.delete(session)
        db.session.commit()
        return 'Could not parse user details', 400

    # Check if user exists in DB
    user = User.query.get(user_id)
    if user is None:
        # Add user to database
        user = User(
            id=user_id,
            username=user_name,
            discriminator=user_discriminator
        )
        db.session.add(user)

    # Remove existing sessions for this user
    sessions = Session.query.filter_by(user_id=user_id).all()
    for session in sessions:
        db.session.delete(session)

    # Update session with user ID
    session.user_id = user_id

    # Check for existing credentials
    discord_oauth2 = DiscordOAuth2.query.filter_by(user_id=user_id).first()
    expires_at = datetime.fromtimestamp(time() + int(token_response['expires_in']))
    if discord_oauth2 is None:
        # Store token data in DB
        discord_oauth2 = DiscordOAuth2(
            user_id=user_id,
            access_token=token_response['access_token'],
            refresh_token=token_response['refresh_token'],
            expires_at=expires_at,
            session_id=session.id
        )
        db.session.add(discord_oauth2)
    else:
        # Update existing token data in DB
        discord_oauth2.access_token = token_response['access_token']
        discord_oauth2.refresh_token = token_response['refresh_token']
        discord_oauth2.expires_at = expires_at
        discord_oauth2.session_id = session.id

    # Save changes to DB
    db.session.commit()

    # Return details
    return {
        'session_id': session.id,
        'expires_at': int(session.expires_at.timestamp() * 1000),
        'user': user_details['user']
    }, 200
