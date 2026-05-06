import joblib
from data_loader import load_movie_data
from classes.Recommender import Recommender

print("Step 1: Loading data from movies_clean.csv...")
df = load_movie_data()

rec = Recommender(df)

print("Step 3: Saving to recommender.pkl...")
joblib.dump(rec, "recommender.pkl")

