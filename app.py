"""
app.py — Main Streamlit application for CineMatch AI movie recommender.
"""

import streamlit as st
import joblib

print("DEBUG: App file loaded")


def local_css(file_name):
    """
    Loads a local CSS file and injects it into the Streamlit app.

    Args:
        file_name (str): Path to the CSS file.
    """
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


@st.cache_resource
def get_recommender():
    """
    Loads and caches the precomputed Recommender object from disk.

    Returns:
        Recommender: The loaded Recommender instance.

    Raises:
        FileNotFoundError: If recommender.pkl does not exist.
    """
    try:
        return joblib.load("recommender.pkl")
    except FileNotFoundError:
        st.error("recommender.pkl not found. Please run precompute.py first.")
        st.stop()


def main():
    """Main function that runs the Streamlit CineMatch AI application."""
    print("DEBUG: Main function started")
    st.set_page_config(page_title="CineMatch AI", page_icon="🎬", layout="wide")

    st.title("🎬 CineMatch AI")
    st.markdown("### Discover your next favorite movie with the power of Machine Learning")

    with st.spinner("Loading recommender..."):
        recommender = get_recommender()
        df = recommender.df

    tab1, tab2, tab3 = st.tabs(["🎯 By Genre", "🔍 By Plot (AI)", "📊 Dataset"])

    with tab1:
        st.subheader("Filter by Genres")
        all_genres = recommender.get_all_genres()
        selected_genres = st.multiselect("Select genres you like:", all_genres)

        if st.button("Find Movies", key="genre_btn"):
            if not selected_genres:
                st.warning("Please select at least one genre.")
            else:
                try:
                    results = recommender.recommend_by_genre(selected_genres, top_k=6)
                    if not results:
                        st.info("No movies found for selected genres.")
                    else:
                        display_movies(results)
                except Exception as e:
                    st.error(f"Error finding movies: {e}")

    with tab2:
        st.subheader("Describe what you want to watch")
        prompt = st.text_area(
            "Enter a plot description (e.g., 'A space adventure with a hero saving the galaxy')",
            height=100
        )

        if st.button("Get Recommendations", key="plot_btn"):
            if not prompt.strip():
                st.warning("Please enter a description.")
            else:
                try:
                    results = recommender.recommend_by_description(prompt, top_k=6)
                    if not results:
                        st.info("No close matches found. Try a different description.")
                    else:
                        display_movies(results)
                except Exception as e:
                    st.error(f"Error getting recommendations: {e}")

    with tab3:
        st.subheader("Explore the Dataset")
        st.caption(f"Showing 500 of {len(df)} rows")
        st.dataframe(df.head(500), width='stretch')


def display_movies(movies):
    """
    Displays a list of Movie objects as styled cards in the Streamlit UI.

    Args:
        movies (list): List of Movie objects to display.
    """
    st.markdown("<br>", unsafe_allow_html=True)

    for i in range(0, len(movies), 2):
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(movies):
                movie = movies[i + j]
                with cols[j]:
                    st.markdown(f"""
                    <div class="movie-card">
                        <div class="movie-title">{movie.title}</div>
                        <div class="movie-genres">{movie.genres.replace('|', ' • ')}</div>
                        <div class="movie-description">{movie.description}</div>
                        <div class="movie-tagline"><i>{movie.tagline}</i></div>
                    </div>
                    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()