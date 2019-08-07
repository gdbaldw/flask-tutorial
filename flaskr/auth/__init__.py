from flask import Blueprint, g
from flask_login import LoginManager

from ..models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

from . import routes


login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return g.session.query(User).get(int(user_id))

login_manager.login_view = "auth.login"
