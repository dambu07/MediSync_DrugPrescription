import streamlit as st
import pickle
from pandas import DataFrame
import json
from streamlit_lottie import st_lottie

st.title("Tailored for Pharmaceutical Enterprises")

#define columns
col1, col2 = st.columns([1.5,1])

with col1:
    drugs_dict = pickle.load(open('drugs_dict.pkl','rb'))
    drugs = DataFrame(drugs_dict)


    #Lets Calculate an Effective Rating
    min_rating = drugs['rating'].min()
    max_rating = drugs['rating'].max()

    def scale_rating(rating):
        rating -= min_rating
        rating = rating / (max_rating - 1)
        rating *= 5
        rating = int(round(rating, 0))

        if (int(rating) == 0 or int(rating) == 1 or int(rating) == 2):
            return 0
        else:
            return 1

    drugs['eff_score'] = drugs['rating'].apply(scale_rating)


    # lets also calculate Usefulness Score
    drugs['usefulness'] = drugs['rating']*drugs['usefulCount']*drugs['eff_score']


    # Slider for selecting the number of drugs to display
    num_drugs = st.slider('Select the Number of Drugs to Display:', min_value=1, max_value=100, value=10)

    # Display the top N most useful drugs
    if st.button('Show top drugs'):
        top_drugs = drugs[['drugName', 'condition', 'usefulness']][drugs['usefulness'] > drugs['usefulness'].mean()] \
            .sort_values(by='usefulness', ascending=False).head(num_drugs).reset_index(drop=True)

        st.table(top_drugs)


with col2:
    # animetion from local machine
    def load_lottiefile(filepath: str):
        with open(filepath, "r") as f:
            return json.load(f)


    hello_lottie_local = load_lottiefile("top_drugs.json")

    st_lottie(
        hello_lottie_local,
        speed=1,
        reverse=False,
        loop=True,
        quality="low",  # medium,high
        # renderer = "svg", #canvas
        height=500,
        width=300,
        key=None,
    )
