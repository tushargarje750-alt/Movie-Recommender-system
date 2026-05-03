import pandas as pd
from class_test.Recommender import Recommender

def test_recommender():
    
    print("Loading data...")
    try:
        df = pd.read_csv("movie_data.csv")
    except FileNotFoundError:
        print("Error: movie_data.csv not found.")
        return

    
    print("Initializing Recommender...")
    recommender = Recommender(df)
    
   
    print("\n--- Test 1: Genre Recommendation (Action|Sci-Fi) ---")
    results = recommender.recommend_by_genre(["Action", "Sci-Fi"], top_k=3)
    for m in results:
        print(f"Found: {m.title} ({m.genres})")
    assert len(results) > 0, "Genre recommendation returned no results"

    
    query = "dreams steal secrets"
    print(f"\n--- Test 2: Description Recommendation ('{query}') ---")
    results = recommender.recommend_by_description(query, top_k=3)
    
    found_inception = False
    for m in results:
        print(f"Found: {m.title} - {m.description[:50]}...")
        if "Inception" in m.title:
            found_inception = True
    
    if found_inception:
        print("SUCCESS: Found 'Inception' via description search!")
    else:
        print("WARNING: Did not find 'Inception' in top 3 results.")

   
    query = "asdfghjkl"
    print(f"\n--- Test 3: Gibberish Query ('{query}') ---")
    results = recommender.recommend_by_description(query, top_k=3)
    if len(results) == 0:
        print("SUCCESS: No results for gibberish as expected (due to >0 score filter).")
    else:
        print("Found:", results)

if __name__ == "__main__":
    test_recommender()
