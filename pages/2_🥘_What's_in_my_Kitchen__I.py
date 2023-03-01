from dotenv import load_dotenv
import streamlit as st
import json
import pandas as pd
import redis
import os
import matplotlib.pyplot as plt



st.set_page_config(page_title="What's in my Kitchen?", page_icon="🥘")

st.title("🥘 What's in my Kitchen?")

load_dotenv()
r_host = os.environ.get('RD_HOST')
r_port = os.environ.get('RD_PORT')
r_pass = os.environ.get('RD_PASS')


with open('assets/categories.txt') as c:
    data = c.read()
data = data.replace("'", "\"")
categories = json.loads(data)


@st.cache_data
def redis_call(host, port, password):

    r = redis.Redis(
        host=host,
        port=port,
        password=password)

    keys = r.keys()
    values = r.mget(keys)

    data = {}

    for key, value in zip(keys, values):
        data[f"{key.decode()}"] = f"{value.decode()}"

    return data


data = redis_call(r_host, r_port, r_pass)


df = pd.DataFrame()

for key, value in data.items():
    if key != 'key':
        temp_df = pd.DataFrame.from_dict(json.loads(value), orient='index').T
        temp_df.index = [key]
        df = pd.concat([df, temp_df])
    else:
        pass

st.dataframe(df)


def categorize(categories, grocery_data):
    # create new column
    grocery_data['category'] = ''

    # categorize
    for index, _ in grocery_data.iterrows():
        item_name = index.lower()
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in item_name:
                    grocery_data.at[index, 'category'] = category
                    break

    return grocery_data.sort_values(by='category')


st.dataframe(categorize(categories, df))


def unit_conversion(dataFrame):

    # Convert Kilogram to gram
    dataFrame.loc[dataFrame['Unit'] == 'Kilogram', ['Quantity', 'Unit']] = dataFrame.loc[dataFrame['Unit'] == 'Kilogram', ['Quantity', 'Unit']].replace(
        {'Quantity': {value: value*1000 for value in dataFrame.loc[dataFrame['Unit'] == 'Kilogram', 'Quantity']}, 'Unit': {'Kilogram': 'gram'}})

    # Convert Litre to millilitre
    dataFrame.loc[dataFrame['Unit'] == 'Litre', ['Quantity', 'Unit']] = dataFrame.loc[dataFrame['Unit'] == 'Litre', ['Quantity', 'Unit']].replace(
        {'Quantity': {value: value*1000 for value in dataFrame.loc[dataFrame['Unit'] == 'Litre', 'Quantity']}, 'Unit': {'Litre': 'MilliLitre'}})

    return dataFrame


def plotting(dataFrame, index):

