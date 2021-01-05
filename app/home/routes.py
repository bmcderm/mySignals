from app.home import bp


@bp.route('/')
def home():
    return 'hello world'
