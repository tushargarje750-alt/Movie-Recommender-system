"""
Recommender module providing content-based movie recommendations
using TF-IDF vectorization on movie overviews and taglines.
"""

from classes.Movie import Movie
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pandas as pd


class Recommender:
    """
    Content-based movie recommender system.

    Uses TF-IDF on movie overviews and taglines to recommend movies
    by plot description similarity, and genre matching for genre-based
    recommendations.

    Composition: Recommender is composed of Movie objects returned
    via _row_to_movie().

    Attributes:
        df (DataFrame): The movie dataset.
        tfidf (TfidfVectorizer): Fitted TF-IDF vectorizer.
        tfidf_matrix (sparse matrix): TF-IDF matrix of all movie texts.
    """

    def __init__(self, df):
        """
        Initializes the Recommender by preprocessing data and fitting TF-IDF.

        Args:
            df (DataFrame): Pandas DataFrame containing movie data with
                            columns: id, title, genres, overview, tagline.

        Raises:
            ValueError: If the DataFrame is empty or missing required columns.
        """
        # Validate input
        required_cols = {"id", "title", "genres", "overview"}
        if df is None or df.empty:
            raise ValueError("DataFrame is empty or None.")
        missing = required_cols - set(df.columns)
        if missing:
            raise ValueError(f"DataFrame missing required columns: {missing}")

        self.df = df.copy()

        # Fill missing values
        self.df["genres"] = self.df["genres"].fillna('')
        self.df["overview"] = self.df["overview"].fillna('')
        self.df["tagline"] = self.df["tagline"].fillna('') if "tagline" in self.df.columns else ''

        # Genre list using list comprehension
        self.df["genre_list"] = [
            g.split(", ") if g else [] for g in self.df["genres"]
        ]

        # Combine overview + tagline for richer TF-IDF matching
        self.df["combined_text"] = self.df["overview"] + " " + self.df.get("tagline", '')

        # TF-IDF vectorizer with max_features for performance
        self.tfidf = TfidfVectorizer(stop_words='english', max_features=15000)

        try:
            self.tfidf_matrix = self.tfidf.fit_transform(self.df["combined_text"])
        except Exception as e:
            raise RuntimeError(f"TF-IDF fitting failed: {e}")

    def recommend_by_genre(self, selected_genres, top_k=5):
        """
        Recommends movies matching the selected genres.

        Args:
            selected_genres (list): List of genre strings selected by user.
            top_k (int): Number of top results to return.

        Returns:
            list: List of Movie objects sorted by genre match score.

        Raises:
            TypeError: If selected_genres is not a list.
        """
        if not isinstance(selected_genres, list):
            raise TypeError("selected_genres must be a list.")

        selected_set = set(selected_genres)
        scores = []

        for idx, row in self.df.iterrows():
            movie_genres = set(row["genre_list"])
            match_count = len(selected_set & movie_genres)
            if match_count > 0:
                scores.append((match_count, row))

        # Sort by match count descending
        scores.sort(key=lambda a: a[0], reverse=True)
        return self._build_results(scores, top_k)

    def recommend_by_description(self, query, top_k=5):
        """
        Recommends movies based on a user-provided plot description
        using TF-IDF cosine similarity.

        Args:
            query (str): User's plot description.
            top_k (int): Number of top results to return.

        Returns:
            list: List of Movie objects most similar to the query.

        Raises:
            ValueError: If the query string is empty.
        """
        if not query or not query.strip():
            raise ValueError("Query string cannot be empty.")

        query_vec = self.tfidf.transform([query])
        cosine_sim = linear_kernel(query_vec, self.tfidf_matrix).flatten()
        related_docs_indices = cosine_sim.argsort()[:-top_k - 1:-1]

        results = []
        for idx in related_docs_indices:
            if cosine_sim[idx] > 0:
                results.append(self.df.iloc[idx])

        return self._build_results_from_rows(results)

    def get_all_genres(self):
        """
        Retrieves a sorted set of all unique genres in the dataset.

        Returns:
            list: Sorted list of unique genre strings.
        """
        # Set comprehension — Part 2: set operations
        genre_set = {g for genre_list in self.df["genre_list"] for g in genre_list if g}
        return sorted(genre_set)

    def _build_results(self, scores_and_rows, top_k):
        """
        Builds a list of Movie objects from scored rows.

        Args:
            scores_and_rows (list): List of (score, row) tuples.
            top_k (int): Max number of results.

        Returns:
            list: List of Movie objects.
        """
        return [self._row_to_movie(row) for _, row in scores_and_rows[:top_k]]

    def _build_results_from_rows(self, rows):
        """
        Builds a list of Movie objects from DataFrame rows.

        Args:
            rows (list): List of DataFrame rows.

        Returns:
            list: List of Movie objects.
        """
        return [self._row_to_movie(row) for row in rows]

    def _row_to_movie(self, row):
        """
        Converts a DataFrame row into a Movie object.

        Args:
            row (Series): A single row from the movie DataFrame.

        Returns:
            Movie: A Movie instance populated with row data.
        """
        tagline = row["tagline"] if "tagline" in row.index else ""
        return Movie(
            row["id"],
            row["title"],
            row["genres"],
            row["overview"],
            tagline
        )

    def __len__(self):
        """Returns the total number of movies in the dataset."""
        return len(self.df)