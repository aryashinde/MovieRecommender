                                           ######## Cleaning and Preparing the Dataset ########

# Imported Libraries
import numpy as np
import pandas as pd
import ast
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem.porter import PorterStemmer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

# Read and merge datasets
movie = pd.read_csv("C:\\Users\\Arya Shinde\\PycharmProjects\\faceRecognitionApp\\tmdb_5000_movies.csv")
credit = pd.read_csv("C:\\Users\\Arya Shinde\\PycharmProjects\\faceRecognitionApp\\tmdb_5000_credits.csv")
movie = movie.merge(credit, on ="title")

###########################################################
# Columns needed for the tags:
# genres: drama, sci-fi, horror etc
# id: required for poster picture
# keywords: tags
# title: title always in english, original_title has regional words
# overview: similarity in movies with same gist/summary
# release date how to incorporate??????????
# cast: based on the actors [movies of SRK]
# crew: director [movies of Sanjay Leela Bhansali]
############################################################

# Dataset with columns I want to focus on
movie = movie[['movie_id','title', 'overview','genres','keywords','cast', 'crew']]

# Check for duplicates
movie.duplicated().sum()

# Check for null values and drop
movie.isnull().sum()
movie.dropna(inplace=True) # Directly modifies the dataFrame

# Update genres and keyword column with a list containing only needed values
def returnLists(dicts):
    l=[]
    for i in ast.literal_eval(dicts):
        l.append(i["name"].replace(" ",""))
    return l
movie['genres'] = movie['genres'].apply(returnLists)
movie['keywords'] = movie['keywords'].apply(returnLists)

# Update cast column with a list containing only needed values
def returnLists2(dicts):
    l=[]
    x= ast.literal_eval(dicts)[:3]
    for i in x:
        l.append(i["name"].replace(" ",""))
    return l
movie['cast'] = movie['cast'].apply(returnLists2)

# Update crew column with a list containing only needed values
def director(dicts):
    l=[]
    x= ast.literal_eval(dicts)
    for i in x:
        if i["job"] == "Director":
            l.append(i["name"].replace(" ",""))
            break
    return l
movie['crew'] = movie['crew'].apply(director)

# Update overview column with a list containing previous string values
movie['overview'] =  movie['overview'].apply(lambda x:x.split())

# Created new 'tag' column with all the realted words combined together
movie['tag'] = movie['overview']+movie['genres']+movie['keywords']+movie['cast']+movie['crew']
movie['tag'] = movie['tag'].apply(lambda x:" ".join(x))

# Created a new dataset with needed columns
refined_df = movie[['movie_id','title','tag']]
refined_df.loc[:, 'tag'] = refined_df['tag'].apply(lambda x:x.lower())


                                           ######## Vectorization of the Dataset ########
# Technique used: Bag of words
# Start with less words(5000) for lower dim

# Gets the stem word: ['loved','loving','love'] -> stem is love
ps = PorterStemmer()

# A function to reduce the repeatedwords in 'tag' i.e, replace it with the stem word: ['loved','loving','love'] -> love
def stem(text):
    y=[]
    for i in text.split():
        y.append(ps.stem(i))
    string = " ".join(y)
    return string
refined_df.loc[:, 'tag'] = refined_df['tag'].apply(stem)

# Stop_words removes all kind of stop words like in, to, at from the list
cv = CountVectorizer(max_features=5000,stop_words='english')

# Creates 4806 (movies) x 5000 matrix that keep tracks of each word repition in each movie
vector = cv.fit_transform(refined_df['tag']).toarray()

# Increase in dim, ecludian distance is not good, hence use cosine distance
# Dist inversly propertional to similarity

# Distance between the movies so 4806 x 4806
similar = cosine_similarity(vector)

# Diagnol is 1...similarity with itself is 1

# A function to return first 5 movies close to the movie selected. It sorts the distance matrixin reverse order to return closest 5 movies
def recommend(movie):
    mov_index = refined_df[refined_df['title']==movie].index[0]
    first10 = sorted(list(enumerate(similar[mov_index])),reverse=True,key=lambda x:x[1])[1:11]
    for i in first10:
        print(refined_df.iloc[i[0]].title)

# Creates a file that dumps all the column values to moviesDict
pickle.dump(refined_df.to_dict(),open('moviesDict.pkl','wb'))

# Creates a file that dumps similar matrix values to similar
pickle.dump(similar,open('similar.pkl','wb'))
