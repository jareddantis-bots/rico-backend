from database import create_app, db
from middleware.logger import LoggingMiddleware
from requests import session
from routes import install_routes
from werkzeug.security import generate_password_hash
from yaml import safe_load


# Read config file
try:
    with open('config.yml') as f:
        config = safe_load(f)

    debug = config['app']['debug']
    db_host = config['db']['host']
    db_port = config['db']['port']
    db_user = config['db']['user']
    db_pass = config['db']['password']
    db_name = config['db']['database']
    admin_user = config['app']['admin']['user']
    admin_pass = generate_password_hash(config['app']['admin']['password'])
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
app.config['DISCORD_CALLBACK_URI'] = config['discord']['callback_uri']
app.config['DISCORD_CLIENT_ID'] = config['discord']['client_id']
app.config['DISCORD_CLIENT_SECRET'] = config['discord']['client_secret']


# Create Discord API session
app.config['DISCORD_SESSION'] = session()


# Add routes
app.config['FRONTEND_BASE_URL'] = config['frontend']['base_url']
app.config['API_URL_PREFIX'] = '/v1'
install_routes(app)


# Start Flask app
if __name__ == '__main__':
    if debug:
        app.wsgi_app = LoggingMiddleware(app.wsgi_app)
    app.run(debug=debug)
