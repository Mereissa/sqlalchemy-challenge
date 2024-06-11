from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Measurement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    station = db.Column(db.String)
    date = db.Column(db.String)
    prcp = db.Column(db.Float)
    tobs = db.Column(db.Float)

class Station(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    station = db.Column(db.String)
