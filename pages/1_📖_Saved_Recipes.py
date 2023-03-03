import streamlit as st
import json
import pandas as pd
import openai
from dotenv import load_dotenv
import os

load_dotenv()


st.set_page_config(page_title="Saved Recipes", page_icon="📖")

st.title("📖 Saved Recipes")


with open("./assets/recipes.txt", "r") as f:
    data = f.read()

# data = json.loads(data)

data = data.replace("'", "\"").strip()
list_of_json = data.split('\n\n')

recipe_list, recipe = st.columns([1, 3])

recipe_list.subheader('Recipe List')


recipes = []

for j in list_of_json:
    d = json.loads(j)
    recipes.append(d['recipe_name'])

which_recipe = st.radio(
    "Pick any of the recipes you saved",
    recipes)


recipe.subheader(which_recipe)

prompt = "a guy with rough hair and short beard, wearing a hoody, sitting alone in the woods with his dog and working on his macbook with glowing apple logo. it's night time and full of stars and moon light. give a side view of the guy, not whole face. the photo is taken from a bit far away, like 5-10 meters."

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')


response = openai.Image.create(

    prompt=prompt,

    n=1,

    size="512x512",

)

st.text(response["data"][0]["url"])
