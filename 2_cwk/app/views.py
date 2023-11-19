from flask import render_template, flash
from app import app, models
from datetime import datetime
from .forms import AddMovieForm
import scraper

@app.route('/', methods=['GET', 'POST'])
def home():
    home = {'description': 'Movie review website description'}
    return render_template('home.html', title='Home', home=home)

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