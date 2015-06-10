import uuid
import arrow
from sqlalchemy_utils import UUIDType, ArrowType
from radar.models import db


class Scan(db.Model):
    id = db.Column(UUIDType(binary=False), default=uuid.uuid4, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    added_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_on = db.Column(ArrowType, default=arrow.utcnow, nullable=False)
    updated_on = db.Column(ArrowType, default=arrow.utcnow, nullable=False)
