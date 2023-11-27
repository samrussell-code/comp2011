from app import models, app, db
def movies_to_json(movies):
    '''Easy formatting for movies, reduce size of movie title'''
    return [
        {
            'id': movie.movieID,
            'name': (movie.name[:25] + '...') if len(movie.name) > 25 else movie.name,
            'likes': movie.likes,
        }
        for movie in movies
    ]

def update_rating(movie_id, new_rating):
    ''' called by calculate_rating to update the movie db entry rating to the calculated one'''
    with app.app_context():
        movie = db.session.query(models.Movie).filter(models.Movie.movieID==movie_id).first()
        movie.rating = new_rating
        db.session.commit()

def calculate_rating(movie_id):
    '''This takes the mean of all the ratings in all this movies reviews
       We get all of the reviews, then sum the ratings and divide by the number of review results we found
       Only update the db if necessary, so checks for any change in rating.
    '''
    rating = -1
    reviews = models.Review.query.filter(models.Review.movie_id == movie_id).all()
    movie = models.Movie.query.filter(models.Movie.movieID == movie_id).first()
    old_rating = movie.rating
    rating_sum = 0
    for review in reviews:
        rating_sum+=review.rating
    if reviews:
        rating = rating_sum / len(reviews)
    if old_rating != rating:
        update_rating(movie_id, rating)
    return rating

def update_likes(movie_id):
    '''Since movies store the like counter in their table we need to update this occasionally to match the new user like count
       returns the new like count
       Once again, only update db when necessary, when like count has actually changed.
       likes is calculated by the number of times that movie appears in the UserLikes table
    '''
    movie = models.Movie.query.filter(models.Movie.movieID == movie_id).first()
    old_likes = movie.likes
    new_likes = len(models.UserLike.query.filter(models.UserLike.movie_id == movie_id).all())
    if new_likes != old_likes:
        with app.app_context():
            movie = db.session.query(models.Movie).filter(models.Movie.movieID==movie_id).first()
            movie.likes = new_likes
            db.session.commit()
    return new_likes

def search_constraint(array_2d, max_size):
    '''turns an array of lists into an evenly spaced single list of max size
       this includes constraints to fill out the list with other list elements
       if one sub list is too small.
    '''
    output_list = []
    # maximum size each sublist should have in the final list
    sub_list_max_size = max_size // len(array_2d)
    
    space_remaining = max_size
    lists_too_long = []
    lists_within_range = []
    
    for sublist in array_2d:
        if len(sublist) <= sub_list_max_size:
            space_remaining -= len(sublist)
            lists_within_range.append(sublist)
        else:
            lists_too_long.append(sublist)
    
    space_per_long_list = space_remaining // len(lists_too_long) if len(lists_too_long) > 0 else 0
    for sublist in array_2d:
        if sublist in lists_too_long:
            output_list.extend(sublist[:space_per_long_list])
        elif sublist in lists_within_range:
            output_list.extend(sublist)
    return output_list

def search_query(query):
    '''collects all queries and constraints them into an even list of 15 elements'''
    movie_results = models.Movie.query.filter(models.Movie.name.contains(str(query.movie_name.data))).order_by(models.Movie.likes.desc()).all()
    cast_results = models.CastMember.query.filter(models.CastMember.name.contains(str(query.movie_name.data))).all()    
    user_results = models.User.query.filter(models.User.username.contains(str(query.movie_name.data))).all()
    search_results = search_constraint([movie_results,cast_results,user_results],15)
    return search_results