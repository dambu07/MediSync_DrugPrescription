import streamlit as st
import pickle
from pandas import DataFrame
import json
from streamlit_lottie import st_lottie


#Define the columns
col1, col2 = st.columns([2,1])

with col1:
    st.title("Your Personal Wellness Maestro!")

    # Display Images
    # import Image from pillow to open images
    #img = Image.open("pages/medicine.png")

    # display image using streamlit
    # width is used to set the width of an image
    #st.image(img, width=100)


    drugs_dict = pickle.load(open('drugs_dict.pkl','rb'))
    drugs = DataFrame(drugs_dict)

    # Dropdown for selecting condition
    condition_options = list(drugs['condition'].value_counts().index)
    selected_condition = st.selectbox('Select a Condition:', condition_options)

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


    # Display highest and lowest rated drugs
    if st.button('Show Results'):
        st.subheader('Top 5 Drugs')
        top_drugs = drugs[drugs['condition'] == selected_condition][['drugName', 'usefulness']].sort_values(
            by='usefulness', ascending=False).head().reset_index(drop=True)
        st.table(top_drugs)

        st.subheader('Bottom 5 Drugs')
        bottom_drugs = drugs[drugs['condition'] == selected_condition][['drugName', 'usefulness']].sort_values(
            by='usefulness', ascending=True).head().reset_index(drop=True)
        st.table(bottom_drugs)


with col2:
    # animetion from local machine
    def load_lottiefile(filepath: str):
        with open(filepath, "r") as f:
            return json.load(f)


    hello_lottie_local = load_lottiefile("medicines.json")

    st_lottie(
        hello_lottie_local,
        speed=1,
        reverse=False,
        loop=True,
        quality="low",  # medium,high
        # renderer = "svg", #canvas
        height=250,
        width=250,
        key=None,
    )

