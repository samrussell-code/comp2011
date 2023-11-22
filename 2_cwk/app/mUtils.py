from app import models
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

def search_query(query):
    movie_results = models.Movie.query.filter(models.Movie.name.contains(str(query.movie_name.data))).all()
    cast_results = models.CastMember.query.filter(models.CastMember.name.contains(str(query.movie_name.data))).all()    
    # if there are more than 10 total results
    if len(movie_results)+len(cast_results)>10:
        # we need to remove the number of cast results from movie results, or 5, whichever smaller
        movie_results=movie_results[:(min(5,len(cast_results)))]
    search_results = movie_results + cast_results
    return search_results
    # Pass the movie data to the template