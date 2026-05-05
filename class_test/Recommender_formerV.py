from classes.Movie import Movie

class Recommender:
    def __init__(self, df):
        self.df = df
        # Pre-process genres into lists
        self.df["genre_list"] = self.df["genres"].apply(lambda x: x.split("|"))

    def recommend_by_genre(self, selected_genres, top_k=5):
        selected_set = set(selected_genres)

        scores = []

        for idx, row in self.df.iterrows():
            movie_genres = set(row["genre_list"])
            match_count = len(selected_set & movie_genres)

            if match_count > 0:
                scores.append((match_count, row))

        # Sort by number of matched genres (descending)
        scores.sort(key=lambda x: x[0], reverse=True)

        results = []
        for match_score, movie_row in scores[:top_k]:
            results.append(Movie(
                movie_row["movieId"],
                movie_row["title"],
                movie_row["genres"],
                movie_row["description"]
            ))

        return results
