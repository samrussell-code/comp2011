from app import db

class Expenditure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), index=True)
    date = db.Column(db.DateTime)