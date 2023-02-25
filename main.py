import streamlit as st
import os
import openai
import csv
import json


csv_file = open('Grocery_List.csv', 'r')
json_file = open('grocery_file.json', 'w')

field_names = ("item", "quantity", "unit")
reader = csv.DictReader(csv_file, field_names)

output = []

for row in reader:
    key = row["item"]
    quantity = row["quantity"]
    unit = row["unit"]
    output.append({key: {"quantity": quantity, "unit": unit}})

json.dump(output, json_file, indent=4)

csv_file.close()
json_file.close()


with open('grocery_file.json') as f:
    # Load the contents into a variable
    data = json.load(f)


kitchen_items = data
cuisine = "german"
nutrition = "healthy"
portion = 1
prep_time = "30 minutes"


openai.api_key = os.getenv("OPENAI_API_KEY")

response = openai.Completion.create(
    # model="text-curie-001",
    model="text-davinci-003",
    prompt=f"suggest me a recipe and cooking steps based on the items in this json file {kitchen_items} in {cuisine} style, with {nutrition} nutrition value for {portion} persons within {prep_time}. Don't use all the ingredients. Use the best possible combination economically.",
    temperature=0.7,
    max_tokens=1000,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
)
