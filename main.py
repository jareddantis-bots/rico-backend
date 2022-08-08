from database import create_app, db
from flask import Flask
from routes import install_routes
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


# Add routes
install_routes(app)


# Start Flask app
if __name__ == '__main__':
    app.run(debug=debug)
