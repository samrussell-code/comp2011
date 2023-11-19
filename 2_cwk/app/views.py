from flask import render_template, flash, request
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
    movies = models.Movie.query.order_by(models.Movie.likes.desc()).all()
    movies = movies_to_json(movies)
    # Pass the movie data to the template
    load_more_films = DeleteForm()
    display_count=1
    if load_more_films.validate_on_submit():
        display_count+=1
    return render_template('home.html', title='Home', movies=movies, load_more_films=load_more_films, display_count=display_count*6)

@app.route('/loadmore', methods=['POST'])
def respond():
	data = json.loads(request.data)
	response = data.get('response')
	# Process the response
	return json.dumps({'status': 'OK', 'response': response})

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