from dotenv import load_dotenv
import streamlit as st
import os
import openai
import csv
import json
import pandas as pd
import redis
import hashlib
import socket
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="AI Chef",
    page_icon="🤖")


@st.cache_data
def userid():
    ip_address = socket.gethostbyname(socket.gethostname())
    hash_object = hashlib.sha256(ip_address.encode())
    hex_dig = hash_object.hexdigest()
    user_id = hex_dig[:8]
    return user_id


user_id = userid()

load_dotenv()
r_host = os.environ.get('RD_HOST')
r_port = os.environ.get('RD_PORT')
r_pass = os.environ.get('RD_PASS')


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


st.image("./assets/dalle_cover_lynx.png", use_column_width=True)
st.title("🤖 AI Chef")


data = redis_call(r_host, r_port, r_pass)

OPENAI_API_KEY = st.sidebar.text_input('Your OpenAI API')

cuisine = st.sidebar.selectbox('Type of Cuisine',
                               ["Random", "Chinese", "French", "Greek", "Indian", "Italian", "Japanese", "Korean", "Mexican", "Middle Eastern", "Spanish", "Thai"])

nutrition = st.sidebar.selectbox('Nutrition Target',
                                 ["Any", "Weight Loss", "Balanced", "Muscle Gain", "Cheat Day Meal"])

portion = st.sidebar.select_slider('Number of Portions/People',
                                   options=[1, 2, 3, 4, 5, "custom"])

if portion == "custom":
    portion = st.sidebar.text_input("Number of People")

prep_time = st.sidebar.select_slider('Maximum Preparation Time (in minutes)',
                                     options=[15, 30, 45, 60, 'Unlimited'])

if prep_time == 'Unlimited':
    prep_time = 180


# openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY


@st.cache_data
def recipe_generator(data, cuisine, nutrition, portion, prep_time):
    response = openai.Completion.create(
        # model="text-ada-001",
        model="text-davinci-003",
        prompt=f"Create a recipe and cooking steps based on the items in this json file {data} in {cuisine} cuisine style, with {nutrition} nutrition target in mind. The recipe should be for {portion} persons, only one portion per person and within {prep_time} minutes of preparation and cooking time. Don't use all the ingredients and use the best possible combination economically. give the oil, spices, salt or chillies in minimal amount. provide the total calorie count of the meal. the output should be a valid json format data. the {user_id} is level one, nested inside should be 'recipe_name', nested inside 'recipe_name' should be 'ingredients', 'cooking_steps' and 'calorie_count'. within 'ingredients' there should be nested 'quantity' and 'unit' keys.",
        temperature=0.7,
        max_tokens=750,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response


def is_valid_json(myjson):
    try:
        json.loads(myjson)
    except ValueError:
        return False
    return True


cook = st.sidebar.button('Give me something to Cook!', key='cook')

if cook:
    raw_output = recipe_generator(data, cuisine, nutrition, portion, prep_time)
    recipe = raw_output['choices'][0]['text']
    recipe = recipe.replace("'", "\"")

    if is_valid_json(recipe):
        recipe = json.loads(recipe)

        for user in recipe.keys():

            try:
                st.subheader(f"Recipe Name: {recipe[user]['recipe_name']}")
                st.markdown(
                    f"Calorie Count: {recipe[user]['calorie_count']}\n")

                st.subheader("Ingredients:\n")

                ingredients = recipe[user]['ingredients']

                ing_pretty = "\n".join(
                    [f"- {k}: {v['quantity']} {v['unit']}" if 'unit' in v else f"- {k}: {v}" for k, v in ingredients.items()])

                st.markdown(f"{ing_pretty}\n")

                st.subheader("Cooking Steps:\n")

                steps_pretty = ""
                for step in recipe[user]['cooking_steps']:
                    steps_pretty += f"- {step}\n"

                st.markdown(f"{steps_pretty}\n")

            except:
                st.text(recipe)
    else:
        st.text(recipe)
        
#categorize, unit conversion and visualization
categories = {
    'Bakery': ['durum', 'salt', 'sugar'],
    'Canned goods': ['kidney beans', 'mushroom', 'tomato puree'],
    'Dairy': ['butter', 'cheese', 'egg', 'eggs', 'milk', 'yogurt'],
    'Fish': ['salmon', 'tuna'],
    'Fruits': ['apple', 'orange', 'tangerine'],
    'Grains': ['bread', 'flour', 'musli', 'pasta', 'rice'],
    'Meat': ['beef', 'chicken', 'chicken breast', 'pork'],
    'Oil': ['cooking oil', 'olive oil'],
    'Spices': ['chilli powder', 'garam masala', 'garlic paste', 'garlic powder', 'ginger paste', 'turmeric powder'],
    'Vegetables': ['carrot', 'garlic', 'onion', 'potatoes', 'tomato']   
}

#categories case sensitive
#three catagories liquid, solids and peices ()????

# Load data into a pandas DataFrame
grocery_data = pd.read_csv('Grocery_list_I.csv')

# create new column
grocery_data['Category'] = ''

#categorize
for index, row in grocery_data.iterrows():
    item_name = row['Current Items'].lower()
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in item_name:
                grocery_data.at[index, 'Category'] = category
                break


#Generate updated csv file 
grocery_data.to_csv('categorized_grocery_items.csv', index=False)

categorized_df = pd.read_csv('categorized_grocery_items.csv')
categorized_df_sorted = categorized_df.sort_values(by='Category')

#unit conversion to kilogram
categorized_df_sorted.loc[categorized_df_sorted['Unit'] == 'gram', 'Quantity'] /= 1000
categorized_df_sorted.loc[categorized_df_sorted['Unit'] == 'gram', 'Unit'] = 'Kilogram'

#unit conversion to litre
categorized_df_sorted.loc[categorized_df_sorted['Unit'] == 'MilliLitre', 'Quantity'] /= 1000
categorized_df_sorted.loc[categorized_df_sorted['Unit'] == 'MilliLitre', 'Unit'] = 'Litre'


