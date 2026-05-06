# 🎬 CineMatch AI-Movie Recommender System

A content-based movie recommendation system built with Python and Streamlit. Users can discover movies by selecting preferred genres or describing a plot in natural language. The system uses TF-IDF vectorization and cosine similarity to match user input against a large movie dataset.

---

## 👥 Team Members

| Name | Email | Stevens ID |
|---|---|---|
| Tushar Garje | tgarje@stevens.edu | 20039536
| Anil Telaprolu | atelapro@stevens.edu |  20036954
| Reshikesh Poreddy | rporeddy1@stevens.edu |  20039777

---

## 📌 Project Description

### Problem Statement
Finding a movie to watch can be overwhelming with thousands of options available. CineMatch AI solves this by letting users either select genres they enjoy or describe the kind of movie they want to watch in plain English and instantly getting relevant recommendations.

### Solution Approach
The system uses a **content-based filtering** approach:
- **Genre-based filtering** — matches movies by counting genre overlaps with user-selected genres
- **Plot-based search** — transforms movie overviews and taglines into TF-IDF vectors and ranks them by cosine similarity to the user's description

### ⚠️ Note on Performance
The dataset used in this project is large (300+ MB), so:
- **First load may take 1–2 minutes** while the model is being read into memory
- **After the first load**, all interactions (genre filtering, plot search) are fast
- You will get output please be patient on the first run

---

## 🗂️ Project Structure

```
CineMatch AI-Movie Recommender/
│
├── app.py                  # Main Streamlit web application
├── data_loader.py          # Dataset loading with error handling
├── precompute.py           # One-time script to build and save the model
├── main.ipynb              # Jupyter Notebook demonstrating all features
├── test_recommender.py     # Pytest test cases
├── requirements.txt        # Python dependencies
├── style.css               # Custom UI styling
├── recommender.pkl         # Pre-built TF-IDF model 
├── movies_clean.csv
└── classes/
    ├── Movie.py            # Movie class with operator overloads
    └── Recommender.py      # Recommender class using TF-IDF + cosine similarity


---

## 📦 Dependencies / Libraries

| Library | Purpose |
|---|---|
| `streamlit` | Web UI framework |
| `pandas` | Data loading and preprocessing |
| `scikit-learn` | TF-IDF vectorization and cosine similarity |
| `matplotlib` | Data visualization in notebook |
| `joblib` | Model serialization (save/load `.pkl`) |

---

## ⚙️ How to Run the Program
This repository uses Git LFS for large files (recommender.pkl and movies_clean.csv). Downloading directly from GitHub via "Download ZIP" will give you 1KB pointer files instead of the actual files, and the app will not run.
To run this project correctly:
Use the ZIP file submitted on Canvas it contains the full versions of all large files
### Prerequisites
- Python 3.12 or higher
- All files from the repository including `recommender.pkl`

### Step 1: Install Dependencies
```bash
python -m pip install -r requirements.txt
```

### Step 2: Run the App
```bash
python -m streamlit run app.py
```

The app will open automatically in your browser at:
```
http://localhost:8501
```

> **Note:** The first load may take 1–2 minutes because the model (`recommender.pkl`) is large. This is a one-time wait per session — all subsequent interactions will be fast. Please do not close the terminal while it loads.

## 🔁 Rebuilding the Model (Optional)

The `recommender.pkl` file is already included and ready to use. You only need to rebuild it if you change the dataset. To do so:

```bash
python precompute.py
```

This will refit the TF-IDF model and overwrite `recommender.pkl`.

---

## 🌟 Features

- 🎯 **Genre-based filtering** — select one or more genres to get matching movies
- 🔍 **Plot-based AI search** — describe a movie in natural language and get recommendations
- 📊 **Dataset explorer** — browse the movie dataset directly in the app
- ⚡ **Pre-computed model** — no retraining on every run, fast startup after first load

---

## 👨‍💻 Main Contributions

| Team Member | Contributions |
|---|---|
| **Tushar Garje** | Project architecture, `Recommender.py` (TF-IDF, cosine similarity), `app.py` (Streamlit UI), model precomputation pipeline, exception handling |
| **Anil Telaprolu** | `Movie.py` class design, operator overloads, `test_recommender.py` (Pytest test cases), `data_loader.py` |
| **Reshikesh Poreddy** | Dataset sourcing and cleaning, `main.ipynb` notebook, genre analysis and matplotlib visualizations, README documentation |

---

