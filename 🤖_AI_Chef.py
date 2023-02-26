import streamlit as st
import os
import openai
import csv
import json
import pandas as pd
import redis
import hashlib
import socket

ip_address = socket.gethostbyname(socket.gethostname())
hash_object = hashlib.sha256(ip_address.encode())
hex_dig = hash_object.hexdigest()
user_id = hex_dig[:8]


st.set_page_config(
    page_title="AI Chef",
    page_icon="🤖")

r_host = os.getenv('RD_HOST')
r_port = os.getenv('RD_PORT')
r_pass = os.getenv('RD_PASS')


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
        prompt=f"suggest a recipe and cooking steps based on the items in this json file {data} in {cuisine} cuisine style, with {nutrition} nutrition target in mind. The recipe should be for {portion} persons, only one portion per person and within {prep_time} minutes of preparation and cooking time. Don't use all the ingredients and use the best possible combination economically. give the oil, spices, salt or chillies in minimal amount. Also provide the total calorie count of the meal. the output should be a nested json format data. the user id, recipe name, ingredients, cooking step, calorie count all these should be keys, and the contents should be values.",
        temperature=0.7,
        max_tokens=512,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response


cook = st.sidebar.button('Give me something to Cook!', key='cook')

if cook:
    recipe = recipe_generator(data, cuisine, nutrition, portion, prep_time)
    st.write(recipe['choices'][0]['text'])

    with open("./assets/response_dump.txt", "a") as file:
        file.write(
            f"Inputs:- Cuisine: {cuisine}, Nutrition: {nutrition}, Portion: {portion}, Prep_time: {prep_time}\nOutput:-\n{recipe}\n\n")
