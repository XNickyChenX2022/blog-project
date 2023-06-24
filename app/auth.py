from flask_login import LoginManager
from . import app
from .models import Users

login_manager = LoginManager()
login_manager.login_view = "/login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return Users.query.filter_by(id=id).first()