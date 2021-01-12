import util
import enums
import functools

from config import Config
from oauthlib.oauth2 import InvalidClientIdError
from flask import redirect, url_for, jsonify, session, request


def requireDiscordAuthToken(next: str = ''):
    def decorator(func):
        """
            Makes a route require a Discord auth token.
            This does not check the validity of the token!
            It only checks if it exists.
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            params = {}
            params.update(request.args)
            if next:
                params['next'] = next

            if not util.userHasDiscordAuthToken():
                return redirect(url_for('auth.signin', **params))

            try:
                return func(*args, **kwargs)
            # If the session expired, and the refresh token couldn't be updated,
            # direct them to sign in again
            except InvalidClientIdError:
                return redirect(url_for('auth.logout', next='/signin'))

        return wrapper

    return decorator


def apiRequireDiscordAuthToken(func):
    """
        Makes a route require a Discord auth token.
        This does not check the validity of the token!
        It only checks if it exists. Used for API calls.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not util.userHasDiscordAuthToken():
            return jsonify({
                'status': enums.ServerStatus.ERROR,
                'message': 'user is not authenticated!',
            }), enums.ServerCode.UNAUTHORIZED

        return func(*args, **kwargs)

    return wrapper


def requireAdminRole(func):
    """
        Requires that the route is only accessible
        by an Admin. This passes down 1 variable
        to the route: discordResponse.

        Note: Also requires that the user is authed with Discord.
    """
    @functools.wraps(func)
    @requireDiscordAuthToken()
    def wrapper(*args, **kwargs):
        discordResponse = util.requestDiscordUserInfo()

        # Make sure the user is an Admin
        if discordResponse.discordID not in Config.DISCORD_ADMINS:
            return redirect('/')

        return func(discordResponse, *args, **kwargs)

    return wrapper


def apiRequireAdminRole(func):
    """
        Requires that the route is only accessible
        by an Admin. This passes down 1 variable
        to the route: discordResponse.
        Used for API calls.

        Note: Also requires that the user is authed with Discord.
    """
    @functools.wraps(func)
    @apiRequireDiscordAuthToken
    def wrapper(*args, **kwargs):
        discordResponse = util.requestDiscordUserInfo()

        # Make sure the user is an Admin
        if discordResponse.discordID not in Config.DISCORD_ADMINS:
            return jsonify({
                'status': enums.ServerStatus.ERROR,
            }), enums.ServerCode.UNAUTHORIZED

        return func(discordResponse, *args, **kwargs)

    return wrapper
