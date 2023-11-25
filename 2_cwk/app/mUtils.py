from app import models, app, db
def movies_to_json(movies):
    return [
        {
            'id': movie.movieID,
            'name': (movie.name[:25] + '...') if len(movie.name) > 25 else movie.name,
            'likes': movie.likes,
            # Add other fields as needed
        }
        for movie in movies
    ]

def update_likes(movie_id):
    '''Since movies store the like counter in their table we need to update this occasionally to match the new user like count'''
    movie = models.Movie.query.filter(models.Movie.movieID == movie_id).first()
    old_likes = movie.likes
    new_likes = models.UserLike.query.filter(models.UserLike.movie_id == movie_id).all()
    if len(new_likes) == old_likes:
        return
    with app.app_context():
        movie.likes = len(new_likes)
        db.session.commit()


def search_constraint(array_2d, max_size):
    '''turns an array of lists into an evenly spaced single list of max size
       this includes constraints to fill out the list with other list elements
       if one sub list is too small'''
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
    movie_results = models.Movie.query.filter(models.Movie.name.contains(str(query.movie_name.data))).all()
    cast_results = models.CastMember.query.filter(models.CastMember.name.contains(str(query.movie_name.data))).all()    
    user_results = models.User.query.filter(models.User.username.contains(str(query.movie_name.data))).all()
    # if there are more than 10 total results
    search_results = search_constraint([movie_results,cast_results,user_results],15)
    #if len(movie_results)+len(cast_results) > 10:
        # we need to remove the number of cast results from movie results, or 5, whichever smaller
    #    movie_results=movie_results[:(min(5,len(cast_results)))]
    #search_results = movie_results + cast_results + user_results[:5]
    return search_results
    # Pass the movie data to the template