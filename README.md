# rico-backend

[![Docker Image CI](https://github.com/jareddantis-bots/rico-backend/actions/workflows/build-and-push.yml/badge.svg)](https://github.com/jareddantis-bots/rico-backend/actions/workflows/build-and-push.yml) ![Docker Pulls](https://img.shields.io/docker/pulls/jareddantis/rico-backend)

This is the backend for Rico, a Discord bot for exchanging notes and maintaining threads.
It takes care of communicating with Rico's database, powered by PostgreSQL, and exposes a REST API for interacting with it,
powered by Flask.

It also has the ability to directly communicate with a running instance of Rico using [Nextcord IPC.](https://ipc.docs.nextcord.dev)

Being a backend, it's meant to be used in tandem with both Rico and Rico's frontend/dashboard.
Therefore, when developing locally, it is recommended that one use Docker Compose to run all of Rico's parts together.
Details are on the main [Rico](https://github.com/jareddantis-bots/rico) repository.

## Local development

It is strongly recommended to use Docker Compose to run a local instance of the backend, with this repository's files
mounted as a volume at `/opt/app`, so that you do not have to install Python 3.10 and all of the backend's dependencies
manually, like so:

```yaml
version: '3.8'
services:
  database:
    container_name: rico-db
    image: postgres:alpine
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=rico
    user: postgres
    volumes:
      - rico-db:/var/lib/postgresql/data
    healthcheck:
      test: ['CMD', 'pg_isready']
      interval: 1s
      timeout: 1s
      retries: 3
      start_period: 1s
    restart: always
  backend:
    container_name: rico-backend
    image: jareddantis/rico-backend:latest
    depends_on:
      database:
        condition: service_healthy
    volumes:
      - .:/opt/app
    ports:
      - '5000:5000'
  # frontend, proxy, and bot services here
volumes:
  rico-db:
```

But if you insist, create and enter a virtualenv using

```bash
python3 -m venv .virtualenv
source .virtualenv/bin/activate
```

or, if you're using [pyenv,](https://github.com/pyenv/pyenv)

```bash
# Make sure the virtualenv extension for pyenv is installed
pyenv virtualenv 3.10.5 rico
pyenv shell rico
```

then install all of the backend's dependencies using

```bash
pip install -r requirements.txt
```

Now create a `config.yml` file in the same directory as `main.py` using [this example.](https://github.com/jareddantis-bots/rico/blob/main/backend.config.yml.example)

Then run the backend using

```bash
python main.py
```
