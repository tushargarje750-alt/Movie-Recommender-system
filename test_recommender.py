import pandas as pd
from class_test.Recommender import Recommender

def test_recommender():
    # Load data
    print("Loading data...")
    try:
        df = pd.read_csv("movie_data.csv")
    except FileNotFoundError:
        print("Error: movie_data.csv not found.")
        return