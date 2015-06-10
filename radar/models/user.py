import arrow
from sqlalchemy_utils import IPAddressType, ArrowType
from radar.models import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String, unique=True)
    main_character = db.Column(db.String)
    main_character_id = db.Column(db.Integer)
    alliance_name = db.Column(db.String, nullable=True)
    corporation_name = db.Column(db.String)
    last_ip = db.Column(IPAddressType, default=u'127.0.0.1')
    last_login_on = db.Column(ArrowType, default=lambda: arrow.utcnow())
    anonymous = True
    authenticated = False

    structures = db.relationship('Structure', backref='added_by')
    scans = db.relationship('Scan', backref='added_by')

    def is_authenticated(self):
        return self.authenticated

    def is_active(self):
        return True

    def is_anonymous(self):
        return self.anonymous

    def get_id(self):
        return str  (self.id)
