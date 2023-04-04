import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=7a9f10f0a83cec19f208c70545683ebb&language=en-US".format(movie_id))
    data = response.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):

    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies,recommended_movies_posters

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title("Movie Recommendation System")

selcted_movie = st.selectbox('Enter the movie name',movies['title'].values)

co = movies.loc[movies['title'] == selcted_movie].iloc[0].movie_id
st.image(fetch_poster(co),width=200)
if st.button('Recommend'):
    name, poster = recommend(selcted_movie)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(name[0])
        st.image(poster[0])

    with col2:
        st.text(name[1])
        st.image(poster[1])

    with col3:
        st.text(name[2])
        st.image(poster[2])
    with col4:
        st.text(name[3])
        st.image(poster[3])
    with col5:
        st.text(name[4])
        st.image(poster[4])