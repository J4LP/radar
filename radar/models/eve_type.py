from radar.models import db

class EveType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    structures = db.relationship('Structure', backref='eve_type')

    @classmethod
    def from_text(cls, id, name):
        return cls(id=id, name=name.strip())