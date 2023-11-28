import lottie
import streamlit as st
import json
import requests
from streamlit_lottie import st_lottie


st.set_page_config(
    page_title="MediSync",
    page_icon="💊"
)

#st.sidebar.success("Select a page above")

# Define the columns
col1, col2 = st.columns([1.5, 1])

with col1:
    st.title("Welcome to MediSync")
    st.header("Your Health, Your Way!")
    description_text = """
    Embrace the future of personalized healthcare. 
    Join MediSync and embark on a journey where 
    your prescriptions are as unique as you are. 
    Your health, personalized. Your journey, empowered. 
    Welcome to MediSync — Where Precision Meets Personalization.
    """

    st.text(description_text)

#add medicine.py
    st.button("Explore")



with col2:
    #animetion from local machine
    def load_lottiefile(filepath:str):
        with open(filepath, "r") as f:
            return json.load(f)


    #animetion from url
    #def load_lottieurl(url:str):
        #r = requests.get(url)
        #if r.status_code != 200:
         #   return None
        #return r.json()'''

    #hello_lottie_url = load_lottieurl("https://app.lottiefiles.com/animation/0969293e-77d2-4e5a-a2b4-d90c18ca8abe?channel=web&source=public-animation&panel=download")
    hello_lottie_local = load_lottiefile("hello_man.json")

    st_lottie(
        hello_lottie_local,
        speed=1,
        reverse=False,
        loop=True,
        quality="low", #medium,high
        #renderer = "svg", #canvas
        height=500,
        width=300,
        key=None,
    )


