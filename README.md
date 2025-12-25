
# Asian Drama & Movie Recommender System

<p align="center">

  <a href="https://drama-rec.onrender.com/">
    <img src="https://img.shields.io/badge/🚀_Live_Demo-Asian_Dramas-FF4B4B?style=for-the-badge&logo=render&logoColor=white" alt="Drama Live Link">
  </a>
  <a href="https://movie-rec-cmns.onrender.com/">
    <img src="https://img.shields.io/badge/🚀_Live_Demo-Asian_Movies-008080?style=for-the-badge&logo=render&logoColor=white" alt="Movie Live Link">
  </a>

</p>

A dedicated search and discovery engine for East Asian cinema and television. This project is designed to help users find their next favorite title by analyzing content similarities across various regional databases.



## Data Scope
The databases are curated to include titles released up until **Mid-2025**.

*   **🎬 Movies:** Includes Chinese, Korean, Hong Kong, and Japanese titles.
*   **📺 Dramas:** Includes Chinese, Korean, and Japanese titles.



## Key Features
- **Dual-Engine Discovery:** Separate live sites for episodic dramas and feature films.
- **Regional Filtering:** Users can refine recommendations by selecting specific countries of origin.
- **Content-Based Logic:** Suggestions are generated based on genres, cast, and plot tags.
- **Real-Time Search:** Instant results powered by a lightweight Flask backend.



## How It Works

**Note on Complexity:** This project implements a **basic content-based filtering system**. It is designed for educational and practical search purposes rather than advanced predictive deep learning.

### 1. Simple Content Filtering
The system identifies similarities by looking at the metadata of the titles. Unlike collaborative filtering, which requires user history, this model only uses the attributes of the titles themselves.

### 2. Basic Cosine Similarity
**Cosine Similarity** to measure the relationship between two titles:
- Every drama/movie is converted into a mathematical vector based on its tags.
- The "distance" (angle) between these vectors is calculated.
- Titles with the smallest angle (highest cosine score) are presented as "similar."

### 3. User-Selected Country Filtering
A core feature of this system is the **Country Selection**. Users can choose to restrict recommendations to a specific region (e.g., only Japanese Dramas or only Hong Kong Movies). The system filters the similarity matrix to only return top-ranked results that match the selected country code.


## Tech Stack
- **Framework:** Python (Flask)
- **Data Handling:** Pandas, NumPy
- **ML Basics:** Scikit-Learn (TF-IDF Vectorization, Cosine Similarity)
- **Deployment:** Render


## Project Structure

```bash
├── app.py              # Flask application entry point for dramas
├── movies.py           # Flask application entry point for movies
├── requirements.txt    # Python dependencies
├── app_df.pkl          # Processed model for dramas
├── app_movie_df.pkl    # Processed model for movies
├── comb_sim.pkl        # Pickled similarity scores
├── sim_matrix.npz      # Compressed similarity matrix for scalability
└── templates/          # HTML files for web UI
```





## ⚙️ Installation & Setup

To run this project on your local machine:

### 1. Clone the Repository

```bash
git clone https://github.com/drjollof/drama-recommender.git
cd drama-recommender
```

### 2. Environment Setup

```bash
python -m venv venv

# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies & Run

```bash
pip install -r requirements.txt
python app.py
python movies.py
```

> **Local Access:** View the app at `http://127.0.0.1:5000/`




## Connect  
[LinkedIn](https://www.linkedin.com/in/adesinausman) | [Twitter (X)](https://x.com/Max_D_Don) | [GitHub Profile](https://github.com/drjollof)


*If you find this project helpful for your Asian cinema marathon, please give it a ⭐!*
```
