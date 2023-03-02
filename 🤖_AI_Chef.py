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
import ast

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

def subtruct_ingredients(ingredient_list):
    r = redis.Redis(
        host=r_host,
        port=r_port,
        password=r_pass)
    
    try:
        for item in ingredient_list:
            ing_key = item[0]
            ing_value = int(item[1])

            # temporary fix for Chicken Breas extra space in the key in Redis
            if ing_key == 'Chicken Breast':
                ing_key = 'Chicken Breast '

            redis_value = r.get(ing_key)
            # converting JSON string to Dictionary
            json_data = json.loads(redis_value)
            current_value = float(json_data['quantity'])
            new_value = current_value - ing_value
            json_data['quantity'] = str(new_value)
            # convert dictionary back to JSON string
            new_value_str = json.dumps(json_data)
            # Save updated value back to Redis
            r.set(ing_key, new_value_str)
    except Exception as e:
        st.text(e)
    
    keys = r.keys()
    values = r.mget(keys)

    data = {}

    for key, value in zip(keys, values):
        data[f"{key.decode()}"] = f"{value.decode()}"

    return(data)
    
    


st.image("./assets/dalle_cover_lynx.png", use_column_width=True)
st.title("🤖 AI Chef")


data = redis_call(r_host, r_port, r_pass)

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
if not OPENAI_API_KEY:
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
        prompt=f"Create a recipe and cooking steps based on the items in this json file {data} in {cuisine} cuisine style, with {nutrition} nutrition target in mind. The recipe should be for {portion} persons, only one portion per person and within {prep_time} minutes of preparation and cooking time. Don't use all the ingredients and use the best possible combination economically. give the oil, spices, salt or chillies in minimal amount. provide the total calorie count of the meal per portion. the output should be a dictionary named {user_id}. there should be four keys, 'recipe_name', 'ingredients','cooking_steps' and 'calorie_count'. give 'ingredients' as a list ['ingredient','quantity' ,'unit'], 'cooking_steps' key should be a list of the cooking steps, 'calorie_count' key will have just the calorie value per person.",
        temperature=0.7,
        max_tokens=1000,
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

    try:
        recipe = ast.literal_eval(recipe.split(' = ')[1])

        st.subheader(f"Recipe Name: {recipe['recipe_name']}")
        st.markdown(f"**Calorie Count:** {recipe['calorie_count']}\n")

        st.subheader("Ingredients:\n")

        ingredients = recipe['ingredients']

        ingredients_list = ""
        for item in ingredients:
            ingredients_list += f"* {item[0]}: {item[1]} {item[2]}\n"
        st.markdown(f"{ingredients_list}\n")

        st.subheader("Cooking Steps:\n")

        steps_pretty = ""
        for step in recipe['cooking_steps']:
            steps_pretty += f"- {step}\n"

        st.markdown(f"{steps_pretty}\n")

        # after the action of accepting the cooking step, we need to update the data in redis
        subtruct_ingredients(ingredients)

    except Exception as e:
        st.text('An Exception occured: ', e)
        st.text(recipe.split(' = ')[1])
