class Movie:
    """
    Represents a single movie with its metadata.
    
    Attributes:
        movie_id (int): Unique identifier for the movie.
        title (str): Title of the movie.
        genres (str): Pipe-separated genre string.
        description (str): Plot overview of the movie.
        tagline (str): Short tagline of the movie.
    """

    def __init__(self, movie_id, title, genres, description, tagline=""):
        """
        Constructor for Movie.

        Args:
            movie_id (int): Unique movie ID.
            title (str): Movie title.
            genres (str): Genre string separated by '|' or ', '.
            description (str): Movie overview/plot.
            tagline (str): Short tagline (optional).
        """
        self.movie_id = movie_id
        self.title = title
        self.genres = genres
        self.description = description
        self.tagline = tagline

    def __str__(self):
        """Returns a human-readable string representation of the movie."""
        return f"{self.title} ({self.genres})"

    def __eq__(self, other):
        """
        Checks equality between two Movie objects based on movie_id.

        Args:
            other (Movie): Another Movie object.

        Returns:
            bool: True if both movies have the same movie_id.
        """
        if not isinstance(other, Movie):
            return False
        return self.movie_id == other.movie_id

    def __len__(self):
        """
        Returns the length of the movie description.

        Returns:
            int: Number of characters in the description.
        """
        return len(self.description)

    def get_genre_list(self):
        """
        Splits the genre string into a list of individual genres.

        Returns:
            list: List of genre strings.
        """
        if not self.genres:
            return []
        # Handle both '|' and ', ' separators
        if '|' in self.genres:
            return self.genres.split('|')
        return self.genres.split(', ')