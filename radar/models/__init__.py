import arrow
from flask.ext.login import LoginManager
from flask.ext.migrate import Migrate
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

from .user import User
from .structure import Structure
from .eve_type import EveType
from .solar_system import SolarSystem
from .scan import Scan

login_manager.login_view = 'AccountView:login'


@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return None
    user.anonymous = False
    user.authenticated = True
    return user



@db.event.listens_for(Structure, 'before_update', propagate=True)
def timestamp_before_update(mapper, connection, target):
    target.updated_on = arrow.utcnow()

@db.event.listens_for(Scan, 'before_update', propagate=True)
def timestamp_before_update(mapper, connection, target):
    target.updated_on = arrow.utcnow()
