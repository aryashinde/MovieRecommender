                                                        ######## Webpage ########

# Imported Libraries
import requests
import streamlit as st
import pickle
import pandas as pd

def posterImage(movieID):
    ans = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'.format(movieID))
    data = ans.json()
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']


# A function to return first 5 movies close to the movie selected. It sorts the distance matrixin reverse order to return closest 5 movies
def recommend(movie):
    mov_index = movies[movies['title']==movie].index[0]
    first10 = sorted(list(enumerate(similar[mov_index])),reverse=True,key=lambda x:x[1])[1:11]
    recommended =[]
    recommended_poster=[]
    for i in first10:
        recommended.append(movies.iloc[i[0]].title)
        #API fetch poster image path
        recommended_poster.append(posterImage(movies.iloc[i[0]].movie_id))
    return recommended,recommended_poster

#Reads and reloads moviesDict file and converts it into a dataframe
movieList= pickle.load(open('moviesDict.pkl','rb'))
movies = pd.DataFrame(movieList)

#Reads and reloads similar file
similar = pickle.load(open('similar.pkl','rb'))

# Displays the Title on Webpage
st.title('Movie Recommender')

#Drop down box on the webpage
option = st.selectbox('Enter Search',movies['title'].values)

#Recommend Button and returns list of 10 movies
if st.button('Recommend'):
    names,display = recommend(option)
    col1,col2,col3,col4,col5,col6,col7,col8,col9,col10 = st.columns(10)
    with col1:
        st.text(names[0])
        st.image(display[0])
    with col2:
        st.text(names[1])
        st.image(display[1])
    with col3:
        st.text(names[2])
        st.image(display[2])
    with col4:
        st.text(names[3])
        st.image(display[3])
    with col5:
        st.text(names[4])
        st.image(display[4])
    with col6:
        st.text(names[5])
        st.image(display[5])
    with col7:
        st.text(names[6])
        st.image(display[6])
    with col8:
        st.text(names[7])
        st.image(display[7])
    with col9:
        st.text(names[8])
        st.image(display[8])
    with col10:
        st.text(names[9])
        st.image(display[9])
    for i in display:
        st.write(i)


