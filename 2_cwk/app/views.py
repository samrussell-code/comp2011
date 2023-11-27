from flask import jsonify, redirect, render_template, flash, request, url_for
from flask_login import login_user, logout_user, current_user, login_required
from app import app, models, db
from app.mUtils import movies_to_json, search_query, update_likes, calculate_rating
from .forms import AddMovieForm, ReviewForm, SearchMovieForm, LoginForm, RegisterForm
from sqlalchemy.orm import joinedload
import scraper

COLUMN_COUNT = 4

# This is the about page, minimal functionality and just explains site purpose
@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html', title='Home')

# Main page with infinite scroll movie list, and search bar for movies, cast and users
@app.route('/home', methods=['GET', 'POST'])
def home():
    ''' We set up the movies to be listed, and which ones have been liked by the current user
        This is because the previously liked movies need to be toggled to 'liked'
    '''
    movies = models.Movie.query.order_by(models.Movie.likes.desc()).limit(COLUMN_COUNT).all()
    search = SearchMovieForm()
    movies = movies_to_json(movies) # formatting for title char clamping and easier card implementation
    search_results=[]
    liked_movie_ids = []
    if current_user.is_authenticated:
        liked_movies = models.UserLike.query.filter(models.UserLike.user_id == current_user.userID).all()
        for movie in liked_movies:
            liked_movie_ids.append(movie.movie_id)
    if search.validate_on_submit():
        search_results=search_query(search)
    return render_template('home.html', title='Main Page', movies=movies,search=search, search_results=search_results, liked_movie_ids=liked_movie_ids)

# called by ajax request to toggle a movie to liked and update the db
@app.route('/like_movie/<int:movie_id>', methods=['POST'])
@login_required
def like_movie(movie_id):
    ''' I recognise that these two routes could likely be made into one route but I ran out of time.
        Would implement next time.
        This also returns the like count to be immediately displayed on the ajax response.
        Note that update_likes is called to also update the like counter on the movie model
    '''''
    with app.app_context():
        new_like = models.UserLike(movie_id=movie_id, user_id=current_user.userID)
        db.session.add(new_like)
        db.session.commit()
    likes_count = update_likes(movie_id)
    return jsonify({'likes': likes_count})

# called by ajax request to toggle a movie to liked and update the db
@app.route('/unlike_movie/<int:movie_id>', methods=['POST'])
@login_required
def unlike_movie(movie_id):
    with app.app_context():
        like_to_delete = db.session.query(models.UserLike).filter(models.UserLike.user_id==current_user.userID,models.UserLike.movie_id==movie_id).first()
        db.session.delete(like_to_delete)
        db.session.commit()
    likes_count = update_likes(movie_id)
    return jsonify({'likes': likes_count})

# sub html loaded inside of main page to provide infscroll functionality
@app.route('/movie_card', methods=['GET'])
def messages():
    ''' This route is called each time another COLUMN_COUNT movies want to be loaded
        I have a page counter in infscroll js, which acts as the offset for the db query to take the next set of values
        I also have to apply the same like toggle logic from main to this sub route
    '''
    page = int(request.args.get('page')) # get the page var from js
    movies = models.Movie.query.order_by(models.Movie.likes.desc()).offset((page - 1) * COLUMN_COUNT).limit(COLUMN_COUNT).all()
    movies = movies_to_json(movies)
    liked_movie_ids = []
    if current_user.is_authenticated:
        liked_movies = models.UserLike.query.filter(models.UserLike.user_id == current_user.userID).all()
        for movie in liked_movies:
            liked_movie_ids.append(movie.movie_id)
    return render_template('movie_card.html', movies=movies, liked_movie_ids=liked_movie_ids)

# DEV-ONLY
@app.route('/add_movie', methods=['GET','POST'])
def add_movie():
    '''Have left this in the source code if you wanted to see how my database is pre-populated.
       This interacts with omdbapi which scrapes iMDb for movie information which i populate cast with
       This intentionally has no route for the typical user except directly searching the url, as it is
       not something a user would typically access.
    '''
    add_movie_form = AddMovieForm()
    if add_movie_form.validate_on_submit():
        flash("Movie has already been added!") if scraper.add_movie(add_movie_form.name.data) == -1 else flash("Adding movie...")
    return render_template('add_movie.html', title='Add Movie', add_movie_form=add_movie_form)

# dynurl for each movie in db
@app.route('/movie/<int:movie_id>', methods=['GET'])
def movie(movie_id):
    '''I start off with a get_or_404 to prevent urls of non existent movie_ids causing unwanted errors
       next I check for a current user review so that the jinja conditional adds the delete button to their review
       then we query for all the cast members, this is a many to many relationship so requires the 
    '''
    movie = models.Movie.query.get_or_404(movie_id)
    current_user_like_exist = []
    not_reviewed = True
    if current_user.is_authenticated:
        current_user_like_exist = models.UserLike.query.filter(models.UserLike.user_id==current_user.userID, models.UserLike.movie_id==movie_id).first()
        current_user_review_exist = models.Review.query.filter(models.Review.user_id==current_user.userID).first()
        if current_user_review_exist: not_reviewed = False
    cast_id_list = models.MovieCastMember.query.filter(models.MovieCastMember.movie_id==movie_id).all()
    cast = []
    for moviecast_relation in cast_id_list:
        cast.append(models.CastMember.query.filter(models.CastMember.castMemberID==moviecast_relation.cast_member_id).first())
    # reviews = models.Review.query.filter(models.Review.movie_id==movie_id).all()
    reviews = (
    models.Review.query
    .join(models.User)
    .filter(models.Review.movie_id == movie_id)
    .options(joinedload(models.Review.user))
    .all()
    
)
    rating = calculate_rating(movie_id)
    return render_template('movie.html', name=f'DB {movie.name}', title=movie.name, movie=movie, cast=cast, reviews=reviews, current_user_like_exist=current_user_like_exist, rating=rating, not_reviewed=not_reviewed)

@app.route('/submit_review/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def submit_review(movie_id):
    form = ReviewForm(request.form)
    movie = models.Movie.query.filter(models.Movie.movieID==movie_id).first()
    if form.validate_on_submit():
        new_review = models.Review(user_id=current_user.get_id(),movie_id=movie_id,title=form.title.data,rating=form.rating.data,body=form.body.data)
        with app.app_context():
            db.session.add(new_review)
            db.session.commit()
            flash('Review submitted successfully!', 'success')
        return redirect(url_for('movie', movie_id=movie_id))
    return render_template('submit_review.html', form=form, movie_id=movie_id,  movie=movie, title=str("Review: "+movie.name))

@app.route('/delete_review/<int:review_id>', methods=['POST'])
@login_required
def delete_review(review_id):
    source_page = request.form.get('source_page', 'user')

    # Check if the current user is the owner of the review
    with app.app_context():
        review = db.session.query(models.Review).filter(models.Review.reviewID == review_id).first()
        db.session.delete(review)
        db.session.commit()

    if source_page == 'movie':
        return redirect(url_for('movie', movie_id=review.movie_id))
    else:
        return redirect(url_for('user', user_id=review.user_id))

@app.route('/user/<int:user_id>', methods=['GET'])
def user(user_id):
    user = models.User.query.get_or_404(user_id)
    user_reviews = models.Review.query.filter(models.Review.user_id == user_id).all()
    user_likes = models.UserLike.query.filter(models.UserLike.user_id == user_id).all()
    liked_movies = []
    for like in user_likes:
        liked_movies.append(models.Movie.query.filter(models.Movie.movieID == like.movie_id).first())
    if current_user.is_authenticated:
        title = user.username if user.userID != current_user.userID else 'My Profile'
    else:
        title = user.username
    return render_template('user.html', user=user, title=title, user_reviews=user_reviews, liked_movies=liked_movies)

@app.route('/cast_member/<int:cast_member_id>', methods=['GET'])
def cast_member(cast_member_id):
    cast_member = models.CastMember.query.get_or_404(cast_member_id)
    movie_id_list = models.MovieCastMember.query.filter(models.MovieCastMember.cast_member_id==cast_member_id).all()
    movies = []
    for moviecast_relation in movie_id_list:
        movies.append(models.Movie.query.filter(models.Movie.movieID==moviecast_relation.movie_id).first())
    return render_template('cast_member.html', name=f'DB {cast_member.name}', cast_member=cast_member, movies=movies, title=cast_member.name)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()  # Assuming you have a RegisterForm similar to the LoginForm

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data

        existing_user = models.User.query.filter_by(username=username).first()

        if existing_user:
            flash('Username already exists. Please choose a different username.', 'error')
        else:
            new_user = models.User(username=username, email_address=email)
            new_user.set_password(password)
            with app.app_context():
                db.session.add(new_user)
                db.session.commit()

            if current_user.is_authenticated:
                flash('Registration successful! To log in, please log out of your current account first.', 'success') 
                return redirect(url_for('home'))     
            else:
                flash('Registration successful! You can now log in.', 'success') 
                return redirect(url_for('login'))

    return render_template('register.html', form=form, title='Register')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = models.User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user, force=True)
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html', form=form, title='Login')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('home'))