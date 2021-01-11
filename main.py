import app.models as Models

from config import Config
from app import createApp, DB

app = createApp()


@app.shell_context_processor
def make_shell_context():
    """
        These are the variables automatically imported
        when running `flask shell`, in order to execute
        queries
    """
    return {
        'DB': DB,
        'Signal': Models.Signal,
    }


if __name__ == '__main__':
    app.run()
