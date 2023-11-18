from app import db

class User(db.Model):
    #COLUMNS
    userID = db.Column(db.Integer, index=True, primary_key=True)
    username = db.Column(db.String(500), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    email_address = db.Column(db.String(500), unique=True, nullable=True)
    #RELATIONSHIPS
    user_likes_relation = db.relationship('UserLike', backref='user', lazy=True)
    reviews_relation = db.relationship('Review', backref='user', lazy=True)

class Movie(db.Model):
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

class MovieGenre(db.Model):
    movieGenreID = db.Column(db.Integer, index=True, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.movieID'), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.genreID'), nullable=False)

class Genre(db.Model):
    genreID = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    #RELATIONSHIPS
    movie_genres_relation = db.relationship('MovieGenre', backref='genre', lazy=True)

class MovieCastMember(db.Model):
    movieCastMemberID = db.Column(db.Integer, index=True, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.movieID'), nullable=False)
    cast_member_id = db.Column(db.Integer, db.ForeignKey('cast_member.castMemberID'), nullable=False)

class CastMember(db.Model):
    castMemberID = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.String(500))
    dob = db.Column(db.DateTime)
    #RELATIONSHIPS
    movie_cast_members_relation = db.relationship('MovieCastMember', backref='cast_member', lazy=True)

class Review(db.Model):
    reviewID = db.Column(db.Integer, index=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.userID'))#fk1
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.movieID'))#fk2
    rating = db.Column(db.Integer) # this will be int range 0-100 (representing 0.0-10.0 to 1dp)
    body = db.Column(db.String(5000))

class UserLike(db.Model):
    userLikeID = db.Column(db.Integer, index=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.userID'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.movieID'))