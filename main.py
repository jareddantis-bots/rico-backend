from database import create_app, db
from flask_cors import CORS
from middleware.logger import LoggingMiddleware
from nextcord.ext import ipc
from requests import session
from routes import install_routes
from werkzeug.security import generate_password_hash
from yaml import safe_load


# Read config file
try:
    with open('config.yml') as f:
        config = safe_load(f)

    debug = config['app']['debug']['enabled']
    enable_middleware = config['app']['debug']['middleware_enabled']
    db_host = config['db']['host']
    db_port = config['db']['port']
    db_user = config['db']['user']
    db_pass = config['db']['password']
    db_name = config['db']['database']
    admin_user = config['app']['admin']['user']
    admin_pass = generate_password_hash(config['app']['admin']['password'])
    discord_callback_uri = config['discord']['callback_uri']
    discord_client_id = config['discord']['client_id']
    discord_client_secret = config['discord']['client_secret']
    discord_ipc_host = config['discord']['ipc']['host']
    discord_ipc_port = config['discord']['ipc']['port']
    discord_ipc_secret = config['discord']['ipc']['secret']
except FileNotFoundError:
    raise RuntimeError('config.yml does not exist')
except KeyError as e:
    raise RuntimeError(f'Missing key in config: {e}')
except Exception as e:
    raise RuntimeError(f'Could not read config: {e}')


# Create Flask app and SQLAlchemy instance
app = create_app(__name__, database_uri=f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}')
app.app_context().push()
db.create_all()


# Store basic auth details for bot (admin) user
app.config['ADMIN_USER'] = admin_user
app.config['ADMIN_PASS'] = admin_pass


# Store Discord OAuth2 details
app.config['DISCORD_CALLBACK_URI'] = discord_callback_uri
app.config['DISCORD_CLIENT_ID'] = discord_client_id
app.config['DISCORD_CLIENT_SECRET'] = discord_client_secret


# Create Discord API session and bot websocket client
app.config['DISCORD_SESSION'] = session()
app.config['BOT_IPC'] = ipc.client.Client(
    host=discord_ipc_host,
    port=discord_ipc_port,
    secret_key=discord_ipc_secret
)


# Enable CORS
api_prefix = config['app']['cors']['prefix']
cors = CORS(app, resources={
    rf'{api_prefix}/*': {
        'origins': config['app']['cors']['origin'],
        'allow_headers': ['authorization', 'content-type']
    }
})


# Add routes
app.config['API_URL_PREFIX'] = api_prefix
install_routes(app)


# Start Flask app
if __name__ == '__main__':
    if enable_middleware:
        app.wsgi_app = LoggingMiddleware(app.wsgi_app)
    app.run(debug=debug)
