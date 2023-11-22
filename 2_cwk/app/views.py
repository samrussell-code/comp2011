from flask import jsonify, render_template, flash, request
from app import app, models
from datetime import datetime
from app.mUtils import movies_to_json
from .forms import AddMovieForm, DeleteForm, SearchMovieForm
import scraper, json, logging

COLUMN_COUNT = 4

@app.route('/', methods=['GET', 'POST'])
def home():
    # Query all movies ordered by likes in descending order
    app.logger.info('index route request')
    movies = models.Movie.query.limit(COLUMN_COUNT).all()
    search = SearchMovieForm()
    movies = movies_to_json(movies)
    search_results=[]
    if search.validate_on_submit():
        search_results = models.Movie.query.filter(models.Movie.name.contains(str(search.movie_name.data))).all()
    # Pass the movie data to the template
    return render_template('home.html', title='Home', movies=movies,search=search, search_results=search_results)

# route to infscroll home page
@app.route('/movie_card', methods=['GET'])
def messages():
    page = int(request.args.get('page')) # get the page var from js
    movies = models.Movie.query.offset((page - 1) * COLUMN_COUNT).limit(COLUMN_COUNT).all()
    movies = movies_to_json(movies)
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
    cast_id_list = models.MovieCastMember.query.filter(models.MovieCastMember.movie_id==movie_id).all()
    cast = []
    for moviecast_relation in cast_id_list:
        cast.append(models.CastMember.query.filter(models.CastMember.castMemberID==moviecast_relation.cast_member_id).first())
    return render_template('movie.html', name=f'DB {movie.name}', movie=movie, cast=cast)