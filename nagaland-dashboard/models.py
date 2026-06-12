# models.py
from database import db

class District(db.Model):
    __tablename__ = 'districts'

    id   = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    stats = db.relationship('RegistrationStat', backref='district', lazy=True)


class RegistrationStat(db.Model):
    __tablename__ = 'registration_stats'

    id                       = db.Column(db.Integer, primary_key=True)
    district_id              = db.Column(db.Integer, db.ForeignKey('districts.id'), nullable=False)
    area_type                = db.Column(db.String(10), nullable=False)
    year                     = db.Column(db.Integer, nullable=False)
    census_population        = db.Column(db.Integer)
    reg_units                = db.Column(db.Integer)
    returns_due              = db.Column(db.Integer)
    returns_received         = db.Column(db.Integer)
    est_midyear_pop_total    = db.Column(db.Float)
    est_midyear_pop_adjusted = db.Column(db.Integer)