import csv
import pandas as pd
import matplotlib.pyplot as plt

categories = {
        'Bakery': ['durum', 'salt', 'sugar', 'bread'],
        'Canned goods': ['kidney beans', 'mushroom', 'tomato puree'],
        'Dairy': ['butter', 'cheese', 'egg', 'eggs', 'milk', 'yogurt'],
        'Fish': ['salmon', 'tuna'],
        'Fruits': ['apple', 'orange', 'tangerine'],
        'Grains': ['flour', 'musli', 'pasta', 'rice'],
        'Meat': ['beef', 'chicken', 'chicken breast', 'pork'],
        'Oil': ['cooking oil', 'olive oil'],
        'Spices': ['chilli powder', 'garam masala', 'garlic paste', 'garlic powder', 'ginger paste', 'turmeric powder'],
        'Vegetables': ['carrot', 'garlic', 'onion', 'potatoes', 'tomato']   
    }

def categorize(categories,file_path):
    # Define the rules for categorizing items by keyword

    # Load data into a pandas DataFrame
    grocery_data = pd.read_csv(file_path).set_index("Current Items")
    grocery_data.index.name = None
    # create new column
    grocery_data['Category'] = ''

    #categorize
    for index, row in grocery_data.iterrows():
        item_name = index.lower()
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in item_name:
                    grocery_data.at[index, 'Category'] = category
                    break
    return grocery_data


def sort_catagory(dataFrame):
    dataFrame = dataFrame.sort_values(by='Category')
    return dataFrame



