import string
import random

from flask import session
from config import Config
from requests_oauthlib import OAuth2Session


class DiscordResponse:
    def __init__(self, data: dict):
        self.email = data.get('email', '')
        self.username = data.get('username', '')
        self.discriminator = data.get('discriminator', '')
        self.avatar = data.get('avatar', '')

        try:
            self.discordID = int(data.get('id', 0))
        except ValueError:
            self.discordID = 0

    def isStaff(self) -> bool:
        return self.discordID in Config.DISCORD_STAFF or \
            self.discordID in Config.DISCORD_ADMINS

    def isAdmin(self) -> bool:
        return self.discordID in Config.DISCORD_ADMINS

    def getDiscordProfilePicURL(self) -> str:
        """
            Gets the URL that holds the Discord user's profile picture.
        """
        return buildDiscordProfilePicURL(self.discordID,
                                         self.avatar,
                                         self.getFullUsername())

    def getFullUsername(self) -> str:
        if not self.username or not self.discriminator:
            return ''
        return f'{self.username}#{self.discriminator}'

    def asdict(self):
        return {
            'email': self.email,
            'username': self.username,
            'discriminator': self.discriminator,
            'discordID': self.discordID,
            'avatar': self.avatar,
        }


def buildDiscordProfilePicURL(discordID: str, hash: str, fullDiscordName: str):
    # If we haven't captured their discriminator
    if not fullDiscordName:
        return 'https://cdn.discordapp.com/embed/avatars/0.png'

    discriminator = fullDiscordName.split('#')[1]
    # If the user doesn't have their profile pic,
    # then their profile pic is their discriminator
    # modulo 5, which will generate a random default pic
    if not hash:
        picNum = int(discriminator) % 5
        return f'https://cdn.discordapp.com/embed/avatars/{picNum}.png'

    # If the hash starts with `a_`, then it is a gif
    if hash.startswith('a_'):
        fileType = '.gif'
    else:
        fileType = '.png'

    return f'{Config.DISCORD_AVATAR_CDN_URL}/{discordID}/{hash}{fileType}'


def requestDiscordUserInfo() -> DiscordResponse:
    """
        Checks Discord to see the current user's
        Discord information.
    """
    oauth = createOAuthSession(session[Config.DISCORD_TOKEN_COOKIE])
    d = oauth.get(Config.DISCORD_API + '/users/@me').json()
    return DiscordResponse(d)


def userHasDiscordAuthToken() -> bool:
    """
        Only checks if the user has a Discord auth
        cookie or not. Does not check if the cookie is valid
        or not.
    """
    return bool(session.get(Config.DISCORD_TOKEN_COOKIE))


def createOAuthSession(token: str = None) -> OAuth2Session:
    """
        Creates an OAuth2 session with Discord.
        Also handles token refreshing.
    """
    def tokenUpdater(token: str):
        session[Config.DISCORD_TOKEN_COOKIE] = token

    return OAuth2Session(
        client_id=Config.DISCORD_CLIENT_ID,
        token=token,
        state=session.get(Config.DISCORD_STATE_COOKIE),
        scope=Config.DISCORD_SCOPE,
        redirect_uri=Config.DISCORD_REDIRECT_URI,
        auto_refresh_kwargs={
            'client_id': Config.DISCORD_CLIENT_ID,
            'client_secret': Config.DISCORD_CLIENT_SECRET,
        },
        auto_refresh_url=Config.DISCORD_TOKEN_URL,
        token_updater=tokenUpdater
    )


def generateNone() -> str:
    """
        Generates a nonce.
    """
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
