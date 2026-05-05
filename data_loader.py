import pandas as pd

def load_movie_data(path="movies.csv"):
    return pd.read_csv(path)