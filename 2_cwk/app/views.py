from flask import render_template, flash
from app import app
from datetime import datetime
from .forms import AddMovieForm
import scraper

@app.route('/', methods=['GET', 'POST'])
def home():
    home = {'description': 'You can use this app to manage your money and set goals.'}
    return render_template('home.html', title='Home', home=home)

@app.route('/add_movie', methods=['GET','POST'])
def add_movie():
    add_movie_form = AddMovieForm()
    if add_movie_form.validate_on_submit():
        flash("Movie has already been added!") if scraper.add_movie(add_movie_form.name.data) == -1 else flash("Adding movie...")

    return render_template('add_movie.html', title='Add Movie', add_movie_form=add_movie_form)

@app.route('/movie', methods=['GET','POST'])
def movie():
    movie_title="MOVIE_TITLE"
    release_date= datetime.now()
    rating = -1
    likes = -1
    synopsis = "Synopsis"
    cast = ["Member 1","Member 2"]
    return render_template('movie.html', title='DBMOVIETITLE', movie=movie, movie_title=movie_title, rating=rating, likes=likes, release_date=release_date.strftime("%B %Y"), synopsis=synopsis, cast=cast)
