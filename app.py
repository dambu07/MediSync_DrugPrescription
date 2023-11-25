import streamlit as st
import pickle
from pandas import DataFrame
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


st.title('Drug Prescription System')


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



# Slider for selecting the number of top conditions to display
num_conditions = st.slider('Select the Number of Top Conditions to Display:', min_value=1, max_value=50, value=10)

# Display the most common conditions
if st.button('Show most common conditions'):
    top_conditions = drugs['condition'].value_counts().head(num_conditions)
    st.table(top_conditions)


# Slider for selecting the number of drugs to display
num_drugs = st.slider('Select the Number of Drugs to Display:', min_value=1, max_value=100, value=10)

# Display the top N most useful drugs
if st.button('Show top drugs'):
    top_drugs = drugs[['drugName', 'condition', 'usefulness']][drugs['usefulness'] > drugs['usefulness'].mean()] \
        .sort_values(by='usefulness', ascending=False).head(num_drugs).reset_index(drop=True)

    st.table(top_drugs)



