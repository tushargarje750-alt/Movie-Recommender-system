import streamlit as st
from data_loader import load_movie_data
from classes.Recommender import Recommender


print("DEBUG: App file loaded")

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def main():
    print("DEBUG: Main function started")
    st.set_page_config(page_title="CineMatch AI", page_icon="🎬", layout="wide")

    st.title("🎬 CineMatch AI")
    st.markdown("### Discover your next favorite movie with the power of Machine Learning")

    # Load Data
    with st.spinner("Loading movie database..."):
        df = load_movie_data()
        recommender = Recommender(df)

    # Tabs for different modes
    tab1, tab2, tab3 = st.tabs(["🎯 By Genre", "🔍 By Plot (AI)", "📊 Dataset"])

    with tab1:
        st.subheader("Filter by Genres")
        all_genres = sorted({g for row in df["genres"] for g in row.split("|")})
        selected_genres = st.multiselect("Select genres you like:", all_genres)
        
        if st.button("Find Movies", key="genre_btn"):
            if not selected_genres:
                st.warning("Please select at least one genre.")
            else:
                results = recommender.recommend_by_genre(selected_genres, top_k=6)
                display_movies(results)

    with tab2:
        st.subheader("Describe what you want to watch")
        prompt = st.text_area("Enter a plot description (e.g., 'A space adventure with a hero saving the galaxy')", height=100)
        
        if st.button("Get Recommendations", key="plot_btn"):
            if not prompt.strip():
                st.warning("Please enter a description.")
            else:
                results = recommender.recommend_by_description(prompt, top_k=6)
                if not results:
                    st.info("No close matches found. Try a different description.")
                else:
                    display_movies(results)

    with tab3:
        st.subheader("Explore the Dataset")
        st.dataframe(df, use_container_width=True)

def display_movies(movies):
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Create rows of 3 columns
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
                    </div>
                    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
