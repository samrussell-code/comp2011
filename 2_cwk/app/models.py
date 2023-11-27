from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    #COLUMNS
    userID = db.Column(db.Integer, index=True, primary_key=True)
    username = db.Column(db.String(500), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    email_address = db.Column(db.String(500), unique=True, nullable=True)
    #RELATIONSHIPS
    user_likes_relation = db.relationship('UserLike', backref='user', lazy=True)
    reviews_relation = db.relationship('Review', backref='user', lazy=True)
    #MIXIN FUNCTIONS - inherited for flask-login to work
    def get_id(self): # we need this method as flask-login defaults to PK=id and i want PK=userID
        return str(self.userID)
    def set_password(self, password):
        self.password = generate_password_hash(password)

    # Check if the provided password matches the stored hash
    def check_password(self, password):
        return check_password_hash(self.password, password)

class Movie(db.Model):
    #COLUMNS
    movieID = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    release_date = db.Column(db.DateTime)
    synopsis = db.Column(db.String(5000))
    likes = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    #RELATIONSHIPS
    movie_genres_relation = db.relationship('MovieGenre', backref='movie', lazy=True)
    movie_cast_members_relation = db.relationship('MovieCastMember', backref='movie', lazy=True)
    user_likes_relation = db.relationship('UserLike', backref='movie', lazy=True)
    reviews_relation = db.relationship('Review', backref='movie', lazy=True)

# helper table for mtm relation Movie<->Genre
class MovieGenre(db.Model):
    #COLUMNS
    movieGenreID = db.Column(db.Integer, index=True, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.movieID'), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.genreID'), nullable=False)

class Genre(db.Model):
    #COLUMNS
    genreID = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    #RELATIONSHIPS
    movie_genres_relation = db.relationship('MovieGenre', backref='genre', lazy=True)

# helper table for mtm relation Movie<->CastMember
class MovieCastMember(db.Model):
    #COLUMNS
    movieCastMemberID = db.Column(db.Integer, index=True, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.movieID'), nullable=False)
    cast_member_id = db.Column(db.Integer, db.ForeignKey('cast_member.castMemberID'), nullable=False)

class CastMember(db.Model):
    #COLUMNS
    castMemberID = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.String(500))
    dob = db.Column(db.DateTime)
    #RELATIONSHIPS
    movie_cast_members_relation = db.relationship('MovieCastMember', backref='cast_member', lazy=True)

class Review(db.Model):
    #COLUMNS
    reviewID = db.Column(db.Integer, index=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.userID'))#fk1
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.movieID'))#fk2
    title = db.Column(db.String(125))
    rating = db.Column(db.Integer) # this will be int range 0-100 (representing 0.0-10.0 to 1dp)
    body = db.Column(db.String(5000))

# helper table for mto relation user->like
class UserLike(db.Model):
    #COLUMNS
    userLikeID = db.Column(db.Integer, index=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.userID'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.movieID'))