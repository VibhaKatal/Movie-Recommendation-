import streamlit as st
import pickle
import pandas as pd
import numpy as np

def recommend(movie):
    if movie in movies['title'].values:
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity_matrix[movie_index]
        distances_sorted_indices = distances.argsort()[::-1]
        
        recommended_movies = []
        for i in distances_sorted_indices[1:11]:
            recommended_movies.append(movies.iloc[i].title)
        return recommended_movies
    else:
        return []

movies = pickle.load(open('movies.pkl','rb'))
movies = pd.DataFrame(movies)
st.title("Movie Recommendation")

chunk_size = 1000
with open('similarity_matrix.pkl', 'rb') as f:
    matrix_shape = pickle.load(f)
    similarity_matrix = np.zeros(matrix_shape)
    for i in range(0, matrix_shape[0], chunk_size):
        start = i
        end = min(i + chunk_size, matrix_shape[0])
        chunk = pickle.load(f)
        similarity_matrix[start:end, :] = chunk

option = st.selectbox("Select movie", movies['title'].values)

if st.button("Recommendations"):
    recommended_movies = recommend(option)

    if not recommended_movies:
        st.warning("No recommendations available for the selected movie.")
    else:
        st.write("Recommended movies:")
        for movie in recommended_movies:
            st.write(f"- {movie}")