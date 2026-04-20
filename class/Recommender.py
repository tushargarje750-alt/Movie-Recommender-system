from classes.Movie import Movie

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.metrics.pairwise import linear_kernel

class Recommender:
    def __init__(self, df):
        self.df = df
        
        self.df["genres"] = self.df["genres"].fillna('')
        self.df["genre_list"] = self.df["genres"].apply(lambda a: a.split(", ") if a else [])
        
        self.tfidf = TfidfVectorizer(stop_words='english')
        
        self.df['overview'] = self.df['overview'].fillna('')
        
        self.tfidf_matrix = self.tfidf.fit_transform(self.df['overview'])

    def recommend_by_genre(self, selected_genres, top_k=5):
        selected_set = set(selected_genres)
        scores = []
        for idx, row in self.df.iterrows():
            movie_genres = set(row["genre_list"])
            match_count = len(selected_set & movie_genres)
            if match_count > 0:
                scores.append((match_count, row))

        scores.sort(key=lambda a: a[0], reverse=True)
        
        return self._build_results(scores, top_k)

    def recommend_by_description(self, query, top_k=5):
        
        query_vec = self.tfidf.transform([query])

        cosine_sim = linear_kernel(query_vec, self.tfidf_matrix).flatten()

        related_docs_indices = cosine_sim.argsort()[:-top_k-1:-1]
        
        results = []
        for idx in related_docs_indices:
            
            if cosine_sim[idx] > 0:
                 results.append(self.df.iloc[idx])
        
        return self._build_results_from_rows(results)

    def _build_results(self, scores_and_rows, top_k):
        results = []
        for match_score, movie_row in scores_and_rows[:top_k]:
            results.append(self._row_to_movie(movie_row))
        return results

    def _build_results_from_rows(self, rows):
        return [self._row_to_movie(row) for row in rows]

    def _row_to_movie(self, row):
        return Movie(
            row["id"],
            row["title"],
            row["genres"],
            row["overview"]
        )
