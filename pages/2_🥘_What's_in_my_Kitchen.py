from dotenv import load_dotenv
import streamlit as st
import json
import pandas as pd
import redis
import os
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np


st.set_page_config(page_title="What's in my Kitchen?", page_icon="🥘")

st.title("🥘 What's in my Kitchen?")

load_dotenv()
r_host = os.environ.get('RD_HOST')
r_port = os.environ.get('RD_PORT')
r_pass = os.environ.get('RD_PASS')

df = pd.read_csv('./assets/Grocery_List_Master.csv')

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


def redis2df(redis_json):
    df = pd.DataFrame()

    for key, value in redis_json.items():
        if key != 'key':
            temp_df = pd.DataFrame.from_dict(
                json.loads(value), orient='index').T
            temp_df.index = [key]
            df = pd.concat([df, temp_df])
        else:
            pass
    return df


redis_df = redis2df(data)
redis_df.index.name = 'current items'
# st.dataframe(df)


col1, col2 = st.columns(2)


def categorize(categories, grocery_data):
    # create new column
    grocery_data['category'] = ''

    # categorize
    for index, row in grocery_data.iterrows():
        item_name = row['current items'].lower()
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in item_name:
                    grocery_data.at[index, 'category'] = category
                    break

    return grocery_data.sort_values(by='category')


categorized_list = categorize(categories, df)


def lower_case(dataframe):
    def lower_case_string(s):
        if isinstance(s, str):
            return s.lower()
        else:
            return s
    return dataframe.applymap(lower_case_string)


categorized_list_lowered = lower_case(categorized_list)


def unit_conversion(dataFrame):
    conversion_factors = {
        'kilogram': {'gram': 1000},
        'litre': {'milliLitre': 1000},
        'ounce': {'gram': 28.3495},
        'pound': {'gram': 453.592},
        'teaspoon': {'milliLitre': 4.92892},
        'tablespoon': {'milliLitre': 14.7868},
        'cup': {'milliLitre': 236.588},
    }

    for from_unit, to_units in conversion_factors.items():
        for to_unit, factor in to_units.items():
            mask = (dataFrame['unit'] == from_unit) & (
                dataFrame['unit'] != to_unit)
            dataFrame.loc[mask, 'quantity'] *= factor
            dataFrame.loc[mask, 'unit'] = to_unit
    return dataFrame


categorized_list_lowered_unit_converted_sorted = unit_conversion(
    categorized_list_lowered)


def to_sentence_case(dataFrame):
    for column in dataFrame.select_dtypes(include=['object']):
        dataFrame[column] = dataFrame[column].str.lower().apply(
            lambda x: x.capitalize())
    return dataFrame


categorized_list_lowered_unit_converted_sorted_to_sentence = to_sentence_case(
    categorized_list_lowered_unit_converted_sorted)


def plot(dataFrame):
    colors = {'Bakery': 'rgb(31, 119, 180)',
              'Canned goods': 'rgb(255, 127, 14)',
              'Dairy': 'rgb(44, 160, 44)',
              'Fish': 'rgb(214, 39, 40)',
              'Fruits': 'rgb(148, 103, 189)',
              'Grains': 'rgb(140, 86, 75)',
              'Meat': 'rgb(227, 119, 194)',
              'Oil': 'rgb(127, 127, 127)',
              'Spices': 'rgb(188, 189, 34)',
              'Vegetables': 'rgb(23, 190, 207)'
              }

    piece_df = dataFrame.loc[dataFrame['unit'] == 'Piece']
    gram_df = dataFrame.loc[dataFrame['unit'] == 'gram']
    millilitre_df = dataFrame.loc[dataFrame['unit'] == 'mililitre']

    figs = []

    if not piece_df.empty:
        fig = px.bar(piece_df, x='category', y='quantity', color='current items',
                     color_discrete_map=colors)
        figs.append(fig)

    if not gram_df.empty:
        fig = px.bar(gram_df, x='category', y='quantity', color='current items',
                     color_discrete_map=colors)
        figs.append(fig)

    if not millilitre_df.empty:
        fig = px.bar(millilitre_df, x='category', y='quantity', color='current items',
                     color_discrete_map=colors)
        figs.append(fig)

    for fig in figs:
        col2.plotly_chart(fig)


# st.dataframe(categorized_list_lowered_unit_converted_sorted_to_sentence)
plot(categorized_list_lowered_unit_converted_sorted_to_sentence)


def execute_all_functions(categories, dataFrame):
    a = categorize(categories, dataFrame)
    b = lower_case(a)
    c = unit_conversion(b)
    e = to_sentence_case(c)
    return e


execute_all_functions(categories, df)


# ## Adjusting dataframe after cooking

df1 = categorized_list_lowered_unit_converted_sorted_to_sentence

df2 = pd.read_csv('./assets/Grocery_List__Child.csv')


def all_exe(categories, dataFrame):
    a = categorize(categories, dataFrame)
    b = lower_case(a)
    c = unit_conversion(b)
    e = to_sentence_case(c)
    return e


df3 = execute_all_functions(categories, df2)

merge_df = pd.merge(df1, df3, on='current items',
                    how='outer', suffixes=('_1', '_2'))

# define custom function to adjust quantity


def adjust_quantity(row):
    # get quantities from merged dataframe
    try:
        q1 = row['quantity_1']
    except KeyError:
        q1 = 0
    try:
        q2 = row['quantity_2']
    except KeyError:
        q2 = 0

    # adjust quantity based on values in both dataframes
    return q1 - q2  # subtract quantity of df2 from quantity in df1


with st.form("my_form"):
    st.write("Add new items")
    c1, c2, c3 = st.columns([1, 1, 1])
    item = c1.text_input("Item Name")
    quantity = c2.text_input("Quantity")
    unit = c3.text_input("Unit")

    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
        new_row = pd.DataFrame(
            {'Quantity': quantity, 'Unit': unit}, index=['Current Items'])
        df = df.append(new_row)


# apply custom function to calculate adjusted quantity
merge_df['Quantity'] = merge_df.apply(adjust_quantity, axis=1)

# remove unnecessary columns and rename columns
merge_df.drop(['quantity_1', 'quantity_2', 'unit_2',
              'category_2'], axis=1, inplace=True)
merge_df.rename(columns={'current items': 'Current Items',
                'unit_1': 'Unit', 'category_1': 'Category'}, inplace=True)

merge_df = merge_df.set_index('Current Items')
merge_df = merge_df.reindex(columns=['Quantity', 'Unit', 'Category'])

col1.dataframe(merge_df)
