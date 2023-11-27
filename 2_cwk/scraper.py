# http://www.omdbapi.com/?t={movie_name}&apikey=ff501fc5
# RETURNS
#{"Title":"Guardians of the Galaxy Vol. 2","Year":"2017","Rated":"PG-13","Released":"05 May 2017","Runtime":"136 min","Genre":"Action, Adventure, Comedy","Director":"James Gunn","Writer":"James Gunn, Dan Abnett, Andy Lanning","Actors":"Chris Pratt, Zoe Saldana, Dave Bautista","Plot":"The Guardians struggle to keep together as a team while dealing with their personal family issues, notably Star-Lord's encounter with his father, the ambitious celestial being Ego.","Language":"English","Country":"United States","Awards":"Nominated for 1 Oscar. 15 wins & 60 nominations total","Poster":"https://m.media-amazon.com/images/M/MV5BNjM0NTc0NzItM2FlYS00YzEwLWE0YmUtNTA2ZWIzODc2OTgxXkEyXkFqcGdeQXVyNTgwNzIyNzg@._V1_SX300.jpg","Ratings":[{"Source":"Internet Movie Database","Value":"7.6/10"},{"Source":"Rotten Tomatoes","Value":"85%"},{"Source":"Metacritic","Value":"67/100"}],"Metascore":"67","imdbRating":"7.6","imdbVotes":"738,822","imdbID":"tt3896198","Type":"movie","DVD":"10 Jul 2017","BoxOffice":"$389,813,101","Production":"N/A","Website":"N/A","Response":"True"}


'''This is the code i wrote to take advantage of the omdb API to prepopulate my database with movie and cast information
   It is not used anywhere in the website but may be worth viewing.'''

import requests
from datetime import datetime
from app import app, db, models
from datetime import datetime

movie_titles = []

def get_movie_details(movie_title):
    api_key = 'ff501fc5'
    url = f'http://www.omdbapi.com/?t={movie_title}&plot=full&apikey={api_key}'

    # send request to the OMDB API
    response = requests.get(url)

    # check for success code
    if response.status_code == 200:
        data = response.json()

        movie_title = data.get('Title', 'N/A')
        release_date_string = data.get('Released', 'N/A')

        if release_date_string != 'N/A':
            release_date = datetime.strptime(release_date_string, '%d %b %Y')
        else:
            release_date = None

        rating = data.get('imdbRating', -1)
        likes = -1
        synopsis = data.get('Plot', 'Synopsis not available')
        cast = data.get('Actors', '').split(', ') if data.get('Actors') else ['Cast not available']
        genres = data.get('Genre', '').split(', ') if data.get('Genre') else ['Genre not available']

        return movie_title, release_date, rating, likes, synopsis, cast, genres

    else:
        print(f"Failed to retrieve data from OMDB. Status code: {response.status_code}")
        return None


def add_movie(x):
    movie_title, release_date, rating, likes, synopsis, cast, genres = get_movie_details(x)

    with app.app_context():
        # check if the movie already exists in db (prevent duplicates)
        existing_movie = db.session.query(models.Movie).filter(models.Movie.name == movie_title, models.Movie.synopsis == synopsis).first()
        if existing_movie is None:
            movie_entry = models.Movie(name=movie_title, release_date=release_date, rating=rating, synopsis=synopsis)
            db.session.add(movie_entry)
        else:
            movie_entry = existing_movie
            return -1

        for name in cast:
            existing_cast_member = db.session.query(models.CastMember).filter(models.CastMember.name == name).first()
            if existing_cast_member is None:
                cast_entry = models.CastMember(name=name)
                db.session.add(cast_entry)
                db.session.commit()
            else:
                cast_entry = existing_cast_member

            # add relation to helper table
            existing_movie_cast_member = db.session.query(models.MovieCastMember).filter(models.MovieCastMember.movie_id == movie_entry.movieID, models.MovieCastMember.cast_member_id == cast_entry.castMemberID).first()
            if existing_movie_cast_member is None:
                movie_cast_member = models.MovieCastMember(movie_id=movie_entry.movieID, cast_member_id=cast_entry.castMemberID)
                db.session.add(movie_cast_member)

        for genre_name in genres:
            existing_genre = db.session.query(models.Genre).filter(models.Genre.name == genre_name).first()
            if existing_genre is None:
                genre_entry = models.Genre(name=genre_name)
                db.session.add(genre_entry)
                db.session.commit() 
            else:
                genre_entry = existing_genre

            # add relation to helper table
            existing_movie_genre = db.session.query(models.MovieGenre).filter(models.MovieGenre.movie_id == movie_entry.movieID, models.MovieGenre.genre_id == genre_entry.genreID).first()
            if existing_movie_genre is None:
                movie_genre = models.MovieGenre(movie_id=movie_entry.movieID, genre_id=genre_entry.genreID)
                db.session.add(movie_genre)

        db.session.commit()
