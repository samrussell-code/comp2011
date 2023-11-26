from flask import jsonify, redirect, render_template, flash, request, url_for
from flask_login import login_user, logout_user, current_user, login_required
from app import app, models, db
from app.mUtils import movies_to_json, search_query, update_likes, calculate_rating
from .forms import AddMovieForm, ReviewForm, SearchMovieForm, LoginForm, RegisterForm
from sqlalchemy.orm import joinedload
import scraper

COLUMN_COUNT = 4

@app.route('/', methods=['GET', 'POST'])
def home():
    # Query all movies ordered by likes in descending order
    app.logger.info('index route request')
    movies = models.Movie.query.limit(COLUMN_COUNT).all()
    search = SearchMovieForm()
    movies = movies_to_json(movies)
    search_results=[]
    liked_movie_ids = []
    if current_user.is_authenticated:
        liked_movies = models.UserLike.query.filter(models.UserLike.user_id == current_user.userID).all()
        for movie in liked_movies:
            liked_movie_ids.append(movie.movie_id)
    if search.validate_on_submit():
        search_results=search_query(search)
    return render_template('home.html', title='Home', movies=movies,search=search, search_results=search_results, liked_movie_ids=liked_movie_ids)

@app.route('/like_movie/<int:movie_id>', methods=['POST'])
@login_required
def like_movie(movie_id):
    # Update the likes count in your database or wherever you store it
    # Return the updated likes count
    is_liked = request.form.get('isLiked') == 'true'
    with app.app_context():
        new_like = models.UserLike(movie_id=movie_id, user_id=current_user.userID)
        db.session.add(new_like)
        db.session.commit()
    likes_count = update_likes(movie_id)
    # Return JSON response with updated likes count and a message
    return jsonify({'likes': likes_count})

@app.route('/unlike_movie/<int:movie_id>', methods=['POST'])
@login_required
def unlike_movie(movie_id):
    is_liked = request.form.get('isLiked') == 'false'
    with app.app_context():
        like_to_delete = db.session.query(models.UserLike).filter(models.UserLike.user_id==current_user.userID,models.UserLike.movie_id==movie_id).first()
        db.session.delete(like_to_delete)
        db.session.commit()
    likes_count = update_likes(movie_id)
    # Return JSON response with updated likes count and a message
    return jsonify({'likes': likes_count})

# route to infscroll home page
@app.route('/movie_card', methods=['GET'])
def messages():
    page = int(request.args.get('page')) # get the page var from js
    movies = models.Movie.query.offset((page - 1) * COLUMN_COUNT).limit(COLUMN_COUNT).all()
    movies = movies_to_json(movies)
    liked_movie_ids = []
    if current_user.is_authenticated:
        liked_movies = models.UserLike.query.filter(models.UserLike.user_id == current_user.userID).all()
        for movie in liked_movies:
            liked_movie_ids.append(movie.movie_id)
    return render_template('movie_card.html', movies=movies, liked_movie_ids=liked_movie_ids)

@app.route('/add_movie', methods=['GET','POST'])
def add_movie():
    add_movie_form = AddMovieForm()
    if add_movie_form.validate_on_submit():
        flash("Movie has already been added!") if scraper.add_movie(add_movie_form.name.data) == -1 else flash("Adding movie...")

    return render_template('add_movie.html', title='Add Movie', add_movie_form=add_movie_form)

@app.route('/about', methods=['GET','POST'])
def about():
    return render_template('about.html', title='About')

@app.route('/movie/<int:movie_id>', methods=['GET'])
def movie(movie_id):
    movie = models.Movie.query.get_or_404(movie_id)
    current_user_like_exist = []
    if current_user.is_authenticated:
        current_user_like_exist = models.UserLike.query.filter(models.UserLike.user_id==current_user.userID, models.UserLike.movie_id==movie_id).first()
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
    return render_template('movie.html', name=f'DB {movie.name}', title=movie.name, movie=movie, cast=cast, reviews=reviews, current_user_like_exist=current_user_like_exist, rating=rating)

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