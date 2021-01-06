class ServerStatus:
    OK = 'ok'
    ERROR = 'error'
    MISSING_PARAMETERS = 'missing_parameters'


class ServerCode:
    OK = 200
    CREATED = 201
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404


class ColorCategory:
    PRIMARY = 'primary'
    SUCCESS = 'success'
    DANGER = 'danger'
    INFO = 'info'
    SECONDARY = 'secondary'
    WARNING = 'warning'
    LIGHT = 'light'
    DARK = 'dark'
