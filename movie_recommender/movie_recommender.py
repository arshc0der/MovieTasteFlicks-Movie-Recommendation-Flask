import joblib
import pandas as pd

# Correct paths to model files
kmeans = joblib.load("movie_recommender/kmeans_model.pkl")
scaler = joblib.load("movie_recommender/scaler.pkl")
mlb = joblib.load("movie_recommender/mlb.pkl")
movies = pd.read_csv("movie_recommender/clustered_movies.csv")

def recommend_movies(title, n=10):
    title = title.strip().lower()
    match = movies[movies['title'].str.lower() == title]
    if match.empty:
        return []
    
    cluster_id = match.iloc[0]['cluster']
    similar_movies = movies[
        (movies['cluster'] == cluster_id) &
        (movies['title'].str.lower() != title)
    ]
    
    recommended = similar_movies.sort_values(
        by=['vote_average', 'popularity'],
        ascending=False
    ).head(n)
    
    return recommended[[
        'title', 'vote_average', 'popularity',
        'release_date', 'overview', 'poster_url'
    ]].to_dict(orient='records')

if __name__ == "__main__":
    query = "Iron Man"
    results = recommend_movies(query, n=10)
    if results:
        for movie in results:
            print(f"{movie['title']} ({movie['release_date']})")
            print(f"Rating: {movie['vote_average']} | Popularity: {movie['popularity']}")
            print(f"{movie['overview']}")
            print(f"{movie['poster_url']}")
            print("-" * 40)
    else:
        print("No match found.")
