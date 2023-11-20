from flask import jsonify, render_template, flash, request
from app import app, models
from datetime import datetime
from .forms import AddMovieForm, DeleteForm
import scraper, json

def movies_to_json(movies):
    return [
        {
            'id': movie.movieID,
            'name': movie.name,
            'likes': movie.likes,
            # Add other fields as needed
        }
        for movie in movies
    ]

@app.route('/', methods=['GET', 'POST'])
def home():
    # Query all movies ordered by likes in descending order
    movies = models.Movie.query.limit(5).all()
    movies = movies_to_json(movies)
    # Pass the movie data to the template
    return render_template('home.html', title='Home', movies=movies)

@app.route('/movie_card', methods=['GET'])
def messages():
    page = int(request.args.get('page'))
    movies = models.Movie.query.offset((page - 1) * 5).limit(5).all()
    return render_template('movie_card.html', movies=movies)

@app.route('/add_movie', methods=['GET','POST'])
def add_movie():
    add_movie_form = AddMovieForm()
    if add_movie_form.validate_on_submit():
        flash("Movie has already been added!") if scraper.add_movie(add_movie_form.name.data) == -1 else flash("Adding movie...")

    return render_template('add_movie.html', title='Add Movie', add_movie_form=add_movie_form)

@app.route('/movie/<int:movie_id>', methods=['GET'])
def movie(movie_id):
    movie = models.Movie.query.get_or_404(movie_id)
    return render_template('movie.html', name=f'DB {movie.name}', movie=movie)