import streamlit as st
import pickle
from pandas import DataFrame
import seaborn as sns
import matplotlib.pyplot as plt


drugs_dict = pickle.load(open('drugs_dict.pkl','rb'))
drugs = DataFrame(drugs_dict)

# Popular conditions
popular_conditions = ['Birth Control', 'Depression', 'Pain', 'Anxiety', 'Acne', 'Bipolar Disorde',
                       'Insomnia', 'Weight Loss', 'Obesity', 'ADHD', 'Diabetes, Type 2',
                       'Emergency Contraception', 'High Blood Pressure', 'Migrane']

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


# Filter data based on popular conditions
conditions = drugs[drugs['condition'].isin(popular_conditions)]


custom_colors = ['#F1B4BB','#F99417']


# Create a bar plot
fig, ax = plt.subplots(figsize=(10, 4.3))
sns.barplot(x=conditions['condition'], y=conditions['rating'], hue=conditions['eff_score'], palette=custom_colors, ax=ax)

# Set the background color to black
fig.set_facecolor('#61a3ba')
ax.set_facecolor('#61a3ba')

plt.title('Conditions vs Effective Number of Drugs', color='white')  # Adjusting title color
plt.xticks(rotation=90, color='white')  # Adjusting x-axis label color
plt.ylabel(' ', color='white')  # Adjusting y-axis label color

# Adjusting tick color
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')

# Display the plot
st.pyplot(fig)
