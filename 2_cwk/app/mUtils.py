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