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
    """
test_recommender.py — Pytest test cases for Movie and Recommender classes.
"""

import pytest
import pandas as pd
from classes.Movie import Movie
from classes.Recommender import Recommender


#  Fixtures 

@pytest.fixture
def sample_df():
    """Creates a small sample DataFrame for testing."""
    return pd.DataFrame({
        "id": [1, 2, 3],
        "title": ["Inception", "The Dark Knight", "Interstellar"],
        "genres": ["Action, Sci-Fi", "Action, Crime", "Sci-Fi, Drama"],
        "overview": [
            "A thief who steals corporate secrets through dream-sharing technology.",
            "Batman raises the stakes in his war on crime with the Joker.",
            "A team of explorers travel through a wormhole in space."
        ],
        "tagline": ["Your mind is the scene of the crime.", "Why so serious?", "Mankind was born on Earth."]
    })


@pytest.fixture
def sample_recommender(sample_df):
    """Creates a Recommender instance from the sample DataFrame."""
    return Recommender(sample_df)


#Movie Tests

def test_movie_str():
    """Test __str__ returns correct format."""
    movie = Movie(1, "Inception", "Action, Sci-Fi", "A dream heist movie.")
    assert str(movie) == "Inception (Action, Sci-Fi)"


def test_movie_eq_same_id():
    """Test __eq__ returns True for movies with same ID."""
    m1 = Movie(1, "Inception", "Sci-Fi", "Dream heist.")
    m2 = Movie(1, "Inception Copy", "Sci-Fi", "Different description.")
    assert m1 == m2


def test_movie_eq_different_id():
    """Test __eq__ returns False for movies with different IDs."""
    m1 = Movie(1, "Inception", "Sci-Fi", "Dream heist.")
    m2 = Movie(2, "Interstellar", "Sci-Fi", "Space travel.")
    assert m1 != m2


def test_movie_len():
    """Test __len__ returns length of description."""
    desc = "A dream heist movie."
    movie = Movie(1, "Inception", "Sci-Fi", desc)
    assert len(movie) == len(desc)


def test_movie_get_genre_list():
    """Test genre string is correctly split into a list."""
    movie = Movie(1, "Inception", "Action, Sci-Fi", "A dream heist.")
    genres = movie.get_genre_list()
    assert "Action" in genres
    assert "Sci-Fi" in genres


# Recommender Tests 

def test_recommender_len(sample_recommender):
    """Test __len__ returns correct number of movies."""
    assert len(sample_recommender) == 3


def test_recommend_by_genre_returns_results(sample_recommender):
    """Test genre recommendation returns Movie objects."""
    results = sample_recommender.recommend_by_genre(["Action"], top_k=2)
    assert len(results) > 0
    assert all(hasattr(m, "title") for m in results)


def test_recommend_by_genre_no_match(sample_recommender):
    """Test genre recommendation returns empty list for unknown genre."""
    results = sample_recommender.recommend_by_genre(["Horror"], top_k=2)
    assert results == []


def test_recommend_by_description_returns_results(sample_recommender):
    """Test plot recommendation returns relevant Movie objects."""
    results = sample_recommender.recommend_by_description("space travel wormhole", top_k=2)
    assert len(results) > 0


def test_recommend_by_description_empty_query(sample_recommender):
    """Test that empty query raises ValueError."""
    with pytest.raises(ValueError):
        sample_recommender.recommend_by_description("   ")


def test_recommender_invalid_df():
    """Test that empty DataFrame raises ValueError."""
    with pytest.raises(ValueError):
        Recommender(pd.DataFrame())


def test_get_all_genres(sample_recommender):
    """Test all genres are retrieved as a sorted list."""
    genres = sample_recommender.get_all_genres()
    assert isinstance(genres, list)
    assert "Action" in genres
    assert genres == sorted(genres)
   
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
