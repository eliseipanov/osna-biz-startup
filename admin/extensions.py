from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_admin import Admin
from flask_admin.theme import Bootstrap4Theme

# Shared instances - not bound to app yet
db = SQLAlchemy()
login_manager = LoginManager()
limiter = Limiter(key_func=get_remote_address)

# Admin theme configuration
admin_theme = Bootstrap4Theme(
    swatch='sandstone',
    base_template='admin/master.html'
)

# Admin instance - not bound to app yet
admin = Admin(name='Osna Farm', theme=admin_theme)
