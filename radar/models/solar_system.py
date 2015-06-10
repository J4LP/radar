from radar.models import db

class SolarSystem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    region = db.Column(db.String)
    region_id = db.Column(db.Integer)
    constellation = db.Column(db.String)
    constellation_id = db.Column(db.Integer)

    structures = db.relationship('Structure', backref='system')
