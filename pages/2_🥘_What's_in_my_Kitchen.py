import streamlit as st
import json
import pandas as pd

st.set_page_config(page_title="What's in my Kitchen?", page_icon="🥘")

st.title("🥘 What's in my Kitchen?")

with open('sample data/grocery_file.json') as f:
    # Load the contents into a variable
    data = json.load(f)

df = pd.DataFrame()

for i in range(len(data)):
    for key, value in data[i].items():
        temp_df = pd.DataFrame.from_dict(value, orient='index').T
        temp_df.index = [key]
        df = pd.concat([df, temp_df])

st.dataframe(df)
