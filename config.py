import os

from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    # GENERAL
    LANGUAGES = ['en']
    SECRET_KEY = os.environ['SECRET_KEY']
    DEBUG = bool(int(os.environ.get('DEBUG', 0)))

    # DATABASE
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = 0

    # DISCORD
    DISCORD_SCOPE = ['identify', 'email', 'guilds.join']
    DISCORD_TOKEN_COOKIE = 'discord_token'
    DISCORD_STATE_COOKIE = 'discord_state'
    DISCORD_API = 'https://discordapp.com/api'
    DISCORD_TOKEN_URL = DISCORD_API + '/oauth2/token'
    DISCORD_AUTHORIZE_URL = DISCORD_API + '/oauth2/authorize'
    DISCORD_BOT_TOKEN = os.environ['DISCORD_BOT_TOKEN']
    DISCORD_CLIENT_ID = os.environ['DISCORD_CLIENT_ID']
    DISCORD_CLIENT_SECRET = os.environ['DISCORD_CLIENT_SECRET']
    DISCORD_REDIRECT_URI = os.environ['DISCORD_REDIRECT_URI']
    DISCORD_ADMINS = [int(i) for i in os.environ['DISCORD_ADMINS'].split(',')]
