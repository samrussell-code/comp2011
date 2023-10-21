from app import db

class Expenditure(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), index=True, unique=True, nullable=False)
    amount = db.Column(db.Float, nullable=False)

class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), index=True, unique=True, nullable=False)
    amount = db.Column(db.Float, nullable=False)

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), index=True, nullable=True)
    amount = db.Column(db.Float, nullable=False)