from flask import current_app, request
from middleware.auth import user_only
from models.discord_oauth2 import DiscordOAuth2
from models.session import Session
from typing import Any, TYPE_CHECKING
if TYPE_CHECKING:
    from requests import Session


def get_discord(session_id: str, endpoint: str) -> Any:
    # Get tokens
    session_id = request.cookies.get('session_id')
    discord_oauth2 = DiscordOAuth2.query.filter_by(session_id=session_id).first()
    if discord_oauth2 is None:
        raise Exception('No Discord tokens found')

    # Perform GET request
    sesh: Session = current_app.config['DISCORD_SESSION']
    response = sesh.get(
        url=f'https://discord.com/api/{endpoint}',
        headers={
            'Authorization': f'Bearer {discord_oauth2.access_token}'
        }
    )
    response.raise_for_status()
    return response.json()


@user_only
def get_user_details():
    session_id = request.cookies.get('session_id')

    try:
        return {
            'success': True,
            'me': get_discord(
                session_id=session_id,
                endpoint='users/@me'
            )
        }, 200
    except Exception as e:
        print(e)
        return {
            'success': False,
            'error': str(e)
        }, 400
