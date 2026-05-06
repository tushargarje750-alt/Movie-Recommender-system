"""
data_loader module for loading and validating the movie dataset.
"""

import pandas as pd


def load_movie_data(path="movies_clean.csv"):
    """
    Loads the movie dataset from a CSV file.

    Args:
        path (str): Path to the CSV file. Defaults to 'movies_clean.csv'.

    Returns:
        DataFrame: Pandas DataFrame containing movie data.

    Raises:
        FileNotFoundError: If the file does not exist at the given path.
        ValueError: If the loaded file is empty or missing required columns.
    """
    try:
        df = pd.read_csv(path, usecols=["id", "title", "genres", "overview", "tagline"])
    except FileNotFoundError:
        raise FileNotFoundError(f"Dataset file not found at path: '{path}'. "
                                f"Please ensure movies_clean.csv exists in the project root.")
    except ValueError as e:
        raise ValueError(f"Error reading columns from dataset: {e}")

    # Validate not empty
    if df.empty:
        raise ValueError("The loaded dataset is empty. Please check the CSV file.")

    return df