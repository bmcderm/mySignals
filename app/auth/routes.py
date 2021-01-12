import util
import json
import base64
import app.models as Models

from app import DB
from app.auth import bp
from config import Config
from urllib.parse import urlencode
from enums import ServerCode, ServerStatus
from requests_oauthlib import OAuth2Session
from flask import render_template, session, redirect, url_for, request


@bp.route('/signin', methods=['GET'])
def signin():
    # If we are already have the Discord auth token...
    if util.userHasDiscordAuthToken():
        # Redirect to the license page, which will check if the user
        # has a license already, and will redirect to the proper page
        return redirect(url_for('auth.license'))

    # Initalize an oauth session
    oauth = util.createOAuthSession()

    # Generate a unique state, add a redirect if included
    state = {
        'nonce': util.generateNone(),
    }
    nextUrl = request.args.get('next')
    if nextUrl:
        state.update({'redirect': nextUrl})
    if request.args:
        state.update({'params': request.args})

    state = saveAsState(state)
    loginUrl, state = oauth.authorization_url(
        Config.DISCORD_AUTHORIZE_URL, state=state)
    session[Config.DISCORD_STATE_COOKIE] = state

    return render_template('auth/authWithDiscord.html',
                           title='mySignals Sign In',
                           loginUrl=loginUrl)


@bp.route('/logout', methods=['GET'])
def logout():
    # Remove the cookies
    session.pop(Config.DISCORD_STATE_COOKIE, None)
    session.pop(Config.DISCORD_TOKEN_COOKIE, None)

    if request.args.get('next'):
        return redirect(request.args.get('next'))

    return redirect('/')


@bp.route('/oauth_callback', methods=['GET'])
def discordOAuthCallback():
    # Make sure the state is unaltered
    state = request.args.get('state', '')
    if not state or state != session.get(Config.DISCORD_STATE_COOKIE):
        session.pop(Config.DISCORD_STATE_COOKIE, None)
        return redirect('/')

    oauth = util.createOAuthSession()
    try:
        token = oauth.fetch_token(
            Config.DISCORD_TOKEN_URL,
            client_secret=Config.DISCORD_CLIENT_SECRET,
            authorization_response=request.url,
        )
    except Exception:
        # When the user doesn't auth with Discord
        return redirect('/')

    # Set the cookie with the authorization token
    session[Config.DISCORD_TOKEN_COOKIE] = token

    # If we provided a redirect url, navigate to that instead
    state = getState()
    if state.get('redirect'):
        params = state.get('params', {})
        redir = state.get('redirect')
        if params:
            redir += '?' + urlencode(params)

        return redirect(redir)

    # Go to the user profile on default
    return redirect(url_for('admin.home'))


def saveAsState(state: dict) -> str:
    state = json.dumps(state)
    return base64.b64encode(state.encode()).decode()


def getState() -> dict:
    state = session.get(Config.DISCORD_STATE_COOKIE, '')
    if not state:
        return {}

    # Decode from base64 and convert to dict
    state = base64.b64decode(state).decode()
    return json.loads(state)
