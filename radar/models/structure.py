import uuid
import arrow
import requests
from sqlalchemy_utils import IPAddressType, ArrowType, UUIDType
from radar.models import db
from radar.utils import get_alliance, get_corporation, get_standing
import evelink.char
import evelink.api
from six import itervalues, iterkeys


class Structure(db.Model):

    id = db.Column(UUIDType(binary=False), default=uuid.uuid4, primary_key=True)
    eve_type_id = db.Column(db.Integer, db.ForeignKey('eve_type.id'))
    system_id = db.Column(db.Integer, db.ForeignKey('solar_system.id'))
    planet = db.Column(db.String, nullable=True)
    planet_id = db.Column(db.Integer, nullable=True, default=0)
    corporation = db.Column(db.String, nullable=False)
    corporation_id = db.Column(db.Integer, nullable=False, default=0)
    alliance = db.Column(db.String, nullable=True)
    alliance_id = db.Column(db.Integer, nullable=True)
    standing = db.Column(db.Integer, default=0)
    status = db.Column(db.String, default='Online')
    scan_id = db.Column(UUIDType(binary=False), db.ForeignKey('scan.id'))
    added_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_on = db.Column(ArrowType, default=arrow.utcnow, nullable=False)
    updated_on = db.Column(ArrowType, default=arrow.utcnow, nullable=False)

    scan = db.relationship('Scan')

    @staticmethod
    def update_structures(keys: list):
        Structure.query.delete()
        db.session.commit()
        for key, vcode, character_id in keys:
            api = evelink.api.API(api_key=(key, vcode))
            eve = evelink.eve.EVE()
            character = evelink.char.Char(char_id=character_id, api=api)
            notifications_ids = {notification['id']: notification
                                 for notification in itervalues(character.notifications().result)
                                 if notification['type_id'] in [45, 46, 47, 48, 49]}
            notifications = character.notification_texts(notification_ids=list(iterkeys(notifications_ids)))
            for notification in itervalues(notifications[0]):
                notification_meta = notifications_ids.get(notification['id'])
                if not notification_meta:
                    continue
                if notification_meta['type_id'] == 45:
                    # Alliance anchoring alert
                    if Structure.query.filter_by(eve_type_id=notification['typeID'], system_id=notification['solarSystemID'], planet_id=notification['moonID']).first():
                        continue
                    struct = Structure()
                    if notification['allianceID']:
                        struct.alliance = get_alliance(notification['allianceID'])['name']
                        struct.alliance_id = notification['allianceID']
                        struct.standing = get_standing(notification['allianceID'])
                    else:
                        struct.standing = get_standing(notification['allianceID'])
                    struct.corporation = get_corporation(notification['corpID'])['name']
                    struct.corporation_id = notification['corpID']
                    struct.eve_type_id = notification['typeID']
                    struct.system_id = notification['solarSystemID']
                    struct.planet = eve.character_name_from_id(notification['moonID'])[0]
                    struct.planet_id = notification['moonID']
                    struct.created_on = arrow.get(notification_meta['timestamp'])
                    db.session.add(struct)
                    db.session.flush()
        db.session.commit()


