class Movie:
    def __init__(self, movie_id, title, genres, description):
        self.movie_id = movie_id
        self.title = title
        self.genres = genres
        self.description = description

    def __str__(self):
        return f"{self.title} ({self.genres})"
