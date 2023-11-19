# http://www.omdbapi.com/?t={movie_name}&apikey=ff501fc5
# RETURNS
#{"Title":"Guardians of the Galaxy Vol. 2","Year":"2017","Rated":"PG-13","Released":"05 May 2017","Runtime":"136 min","Genre":"Action, Adventure, Comedy","Director":"James Gunn","Writer":"James Gunn, Dan Abnett, Andy Lanning","Actors":"Chris Pratt, Zoe Saldana, Dave Bautista","Plot":"The Guardians struggle to keep together as a team while dealing with their personal family issues, notably Star-Lord's encounter with his father, the ambitious celestial being Ego.","Language":"English","Country":"United States","Awards":"Nominated for 1 Oscar. 15 wins & 60 nominations total","Poster":"https://m.media-amazon.com/images/M/MV5BNjM0NTc0NzItM2FlYS00YzEwLWE0YmUtNTA2ZWIzODc2OTgxXkEyXkFqcGdeQXVyNTgwNzIyNzg@._V1_SX300.jpg","Ratings":[{"Source":"Internet Movie Database","Value":"7.6/10"},{"Source":"Rotten Tomatoes","Value":"85%"},{"Source":"Metacritic","Value":"67/100"}],"Metascore":"67","imdbRating":"7.6","imdbVotes":"738,822","imdbID":"tt3896198","Type":"movie","DVD":"10 Jul 2017","BoxOffice":"$389,813,101","Production":"N/A","Website":"N/A","Response":"True"}
import requests
from datetime import datetime
from app import app, db, models
movie_titles= ['Donnie Brasco', 'Big Fish', 'Green Book', 'Combat de boxe', 'Duck Soup', 'Amélie', 'Titanic', 'The Grand Budapest Hotel', 'Blood Diamond', '2001: A Space Odyssey', 'Blow', 'Raging Bull', 'A Beautiful Mind', 'Inception', 'Memento', 'Johnny Mad Dog', 'Jurassic Park', 'No Country for Old Men', 'Analyze This', 'Ghostbusters', 'Apocalypse Now', 'The Shawshank Redemption', 'The 400 Blows', 'Mafioso', 'The Town', 'Lawrence of Arabia', 'Avatar', 'Stalag 17', 'The Hurt Locker', 'The Public Enemy', '12 Years a Slave', 'Dr. Strangelove or: How I Learned to Stop Worrying and Love the Bomb', 'Umberto D.', 'Pulp Fiction', 'The Godfather', 'The Green Mile', 'Black Panther', 'Moonlight', 'White Heat', 'American Pie', 'Birdman', 'Donnie Darko', 'The Game', 'The Silence of the Lambs', 'Saving Private Ryan', 'La La Land', 'Ed Wood', 'Catch Me If You Can', 'Back to the Future', 'The Matrix Reloaded', 'E.T. the Extra-Terrestrial', 'Eternal Sunshine of the Spotless Mind', 'The Football Factory', 'Forrest Gump', 'The Sixth Sense', 'Lock, Stock and Two Smoking Barrels', 'The Pianist', 'The Terminator', 'Gone with the Wind', 'Dunkirk', 'Eddie Murphy: Raw', 'The Wolf of Wall Street', 'Citizen Kane', 'The Good, the Bad and the Ugly', 'Old School', '3:10 to Yuma', 'The Business', 'Limitless (I)', 'All Quiet on the Western Front', 'Coming to America', 'Braveheart', 'The Fast and the Furious: Tokyo Drift', 'The Truman Show', 'Once Upon a Time in Hollywood', 'Friday', 'Seven Samurai', 'Star Trek', 'The Dark Knight', 'Field of Dreams', 'The Dirty Dozen', 'Rango', 'The Dark Hours', '1917', 'Batman Begins', '300', 'Wet Hot American Summer', 'Layer Cake', 'The Bellboy', 'Mean Girls', 'Four Lions', 'The Lord of the Rings: The Return of the King', 'The Matrix Revolutions', 'The Breakfast Club', 'Primal Fear', 'Casino Royale', 'The Great Gatsby', 'The Revenant', 'Joker', 'The Avengers', 'Six Shooter', 'Goodfellas', 'Casablanca', 'GoodFellas', 'The Bourne Identity', 'The Dark Knight Rises', 'O Brother, Where Art Thou?', 'Moon', 'Let Him Have It', 'The Errand Boy', 'American History X', 'Groundhog Day', 'The Taking of Pelham One Two Three', 'The Big Lebowski', 'Gladiator', 'In Bruges', 'La haine', 'Up', "Ferris Bueller's Day Off", 'American Beauty', 'Fargo', 'The Social Network', 'The Usual Suspects', 'A Clockwork Orange', 'The Departed', 'Ip Man', 'The Graduate', 'The Hateful Eight', 'Shutter Island', 'The Godfather Part II', 'Psycho', 'Small Time Crooks', 'The Godfather: Part II', 'Heat', 'Nomadland', 'The Shining', 'Raiders of the Lost Ark', 'Parasite', 'CKY2K', 'Dumb and Dumber', 'Fight Club', 'Edmond', 'The Matrix', 'Slumdog Millionaire', 'Gravity', 'The Shape of Water', 'The Martian', 'Trainspotting', 'Inglourious Basterds', 'Interstellar', 'The Fifth Element', 'Mean Streets', 'Belly', "Schindler's List", "Pan's Labyrinth", 'The Wizard of Oz', 'The Irishman', 'The Bourne Supremacy', 'Blade Runner', "One Flew Over the Cuckoo's Nest", 'The Lion King', 'The Boondock Saints', 'Django Unchained', 'Transformers', 'Snatch', 'The Prestige', 'Se7en', 'Star Wars: Episode IV - A New Hope', 'Crash (I)', 'Half Baked', 'Man Bites Dog', 'American Splendor', 'The Longest Day']
# Function to get movie details from OMDB API
def get_movie_details(movie_title):
    api_key = 'ff501fc5'
    url = f'http://www.omdbapi.com/?t={movie_title}&apikey={api_key}'

    # Send an HTTP request to the OMDB API
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON content of the response
        data = response.json()

        # Extract relevant information
        movie_title = data.get('Title', 'N/A')
        release_date = datetime.strptime(data.get('Released', ''), '%d %b %Y') if not data.get('Released','N/A') else datetime.now()
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
        # Check if the movie already exists
        existing_movie = db.session.query(models.Movie).filter(models.Movie.name == movie_title, models.Movie.synopsis == synopsis).first()
        if existing_movie is None:
            # Movie does not exist, add it
            movie_entry = models.Movie(name=movie_title, release_date=release_date, rating=rating, synopsis=synopsis)
            db.session.add(movie_entry)
        else:
            movie_entry = existing_movie
            return -1

        # Check and add cast members
        for name in cast:
            existing_cast_member = db.session.query(models.CastMember).filter(models.CastMember.name == name).first()
            if existing_cast_member is None:
                # Cast member does not exist, add them
                cast_entry = models.CastMember(name=name)
                db.session.add(cast_entry)
                db.session.commit()  # Commit here to get the new cast_member_id
            else:
                cast_entry = existing_cast_member

            # Check if the cast is already associated with the movie
            existing_movie_cast_member = db.session.query(models.MovieCastMember).filter(models.MovieCastMember.movie_id == movie_entry.movieID, models.MovieCastMember.cast_member_id == cast_entry.castMemberID).first()
            if existing_movie_cast_member is None:
                # Associate cast with the movie
                movie_cast_member = models.MovieCastMember(movie_id=movie_entry.movieID, cast_member_id=cast_entry.castMemberID)
                db.session.add(movie_cast_member)

        # Check and add genres
        for genre_name in genres:
            existing_genre = db.session.query(models.Genre).filter(models.Genre.name == genre_name).first()
            if existing_genre is None:
                # Genre does not exist, add it
                genre_entry = models.Genre(name=genre_name)
                db.session.add(genre_entry)
                db.session.commit()  # Commit here to get the new genre_id
            else:
                genre_entry = existing_genre

            # Check if the genre is already associated with the movie
            existing_movie_genre = db.session.query(models.MovieGenre).filter(models.MovieGenre.movie_id == movie_entry.movieID, models.MovieGenre.genre_id == genre_entry.genreID).first()
            if existing_movie_genre is None:
                # Associate genre with the movie
                movie_genre = models.MovieGenre(movie_id=movie_entry.movieID, genre_id=genre_entry.genreID)
                db.session.add(movie_genre)

        db.session.commit()

#count = 0
#for x in movie_titles:
#    print("#" + str(count) + ":", x)
#    count += 1
#    add_movie(x)

