from app import db


class User(db.Model):
    userID = db.Column(db.Integer, index=True, primary_key=True)
    username = db.Column(db.String(500), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    email_address = db.Column(db.String(500), unique=True, nullable=True)

class Review(db.Model):
    reviewID = db.Column(db.Integer, index=True, primary_key=True)
    user_id = db.Column(db.Integer)#fk1
    movie_id = db.Column(db.Integer)#fk2
    rating = db.Column(db.Integer) # this will be int range 0-100 (representing 0.0-10.0 to 1dp)
    body = db.Column(db.String(5000))