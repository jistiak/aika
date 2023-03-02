# %%
from dotenv import load_dotenv
import streamlit as st
import json
import pandas as pd
import redis
import os
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np


## Categorize, Unit conversion

grocery_list = pd.read_csv('D:\Codes\lynx_ai\Shariar\Grocery_List_Master.csv') 

categories = {
        'Bakery': ['durum', 'salt', 'sugar', 'bread'],
        'Canned goods': ['tomato puree','kidney beans', 'mushroom', ],
        'Dairy': ['butter', 'cheese', 'egg', 'eggs', 'milk', 'yogurt'],
        'Fish': ['salmon', 'tuna'],
        'Fruits': ['apple', 'orange', 'tangerine'],
        'Grains': ['flour', 'musli', 'pasta', 'rice'],
        'Meat': ['beef', 'chicken', 'chicken breast', 'pork','sausage'],
        'Oil': ['cooking oil', 'olive oil'],
        'Spices': ['garlic paste','chilli powder', 'garam masala',  'garlic powder', 'ginger paste', 'turmeric powder'],
        'Vegetables': ['carrot', 'onion', 'garlic' ,'potatoes', 'tomato']   
    }

def categorize(categories, dataFrame):
    # create new column
    dataFrame['category'] = ''

    # categorize
    for index, _ in dataFrame.iterrows():
        item_name = dataFrame.iloc[index]['current items'].lower()
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in item_name:
                    dataFrame.at[index, 'category'] = category
                    break

    return dataFrame

catagorized_list = categorize(categories, grocery_list)

def lower_case(dataframe):
    def lower_case_string(s):
        if isinstance(s, str):
            return s.lower()
        else:
            return s
    return dataframe.applymap(lower_case_string)

catagorized_list_lowered = lower_case(catagorized_list)

def unit_conversion(dataFrame):
    conversion_factors = {
        'kilogram': {'gram': 1000},
        'litre': {'milliLitre': 1000},
        'ounce': {'gram': 28.3495},
        'pound': {'gram': 453.592},
        'teaspoon': {'milliliter': 4.92892},
        'tablespoon': {'milliliter': 14.7868},
        'cup': {'milliliter': 236.588},
    }

    for from_unit, to_units in conversion_factors.items():
        for to_unit, factor in to_units.items():
            mask = (dataFrame['unit'] == from_unit) & (dataFrame['unit'] != to_unit)
            dataFrame.loc[mask, 'quantity'] *= factor
            dataFrame.loc[mask, 'unit'] = to_unit
    return dataFrame

catagorized_list_lowered_unit_converted = unit_conversion(catagorized_list_lowered)

def sort_catagory(dataFrame):
    dataFrame = dataFrame.sort_values(by='category')
    return dataFrame

catagorized_list_lowered_unit_converted_sorted = sort_catagory(catagorized_list_lowered_unit_converted)

def to_sentence_case(dataFrame):
    for column in dataFrame.select_dtypes(include=['object']):
        dataFrame[column] = dataFrame[column].str.lower().apply(lambda x: x.capitalize())
    return dataFrame

catagorized_list_lowered_unit_converted_sorted_to_sentence = to_sentence_case(catagorized_list_lowered_unit_converted_sorted)

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
    gram_df = dataFrame.loc[dataFrame['unit'] == 'Gram']
    millilitre_df = dataFrame.loc[dataFrame['unit'] == 'Millilitre']
    
    if not piece_df.empty:
        fig1 = px.bar(piece_df, x='category', y='quantity', color='current items',color_discrete_sequence=px.colors.qualitative.Pastel)
        
    if not gram_df.empty:   
        fig2 = px.bar(gram_df, x='category', y='quantity', color='current items',color_discrete_sequence=px.colors.qualitative.Pastel)
        
    if not millilitre_df.empty:
        fig3 = px.bar(millilitre_df, x='category', y='quantity', color='current items',color_discrete_sequence=px.colors.qualitative.Pastel)

    fig1.show()
    fig2.show()
    fig3.show()
    
plot(catagorized_list_lowered_unit_converted_sorted_to_sentence)

def execute_all_functions(categories, dataFrame):
   a = categorize(categories, dataFrame)
   b = lower_case(a)
   c = unit_conversion(b)
   d = sort_catagory(c)
   e = to_sentence_case(d)
   return e

execute_all_functions(categories, grocery_list)


# ## Adjusting dataframe after cooking

df1 = catagorized_list_lowered_unit_converted_sorted_to_sentence

df2 = pd.read_csv('D:\Codes\lynx_ai\Shariar\Grocery_List__Child.csv')

def all_exe(categories, dataFrame):
   a = categorize(categories, dataFrame)
   b = lower_case(a)
   c = unit_conversion(b)
   d = sort_catagory(c)
   e = to_sentence_case(d)
   return e
   
df3 = execute_all_functions(categories, df2)

merge_df = pd.merge(df1, df3, on='current items', how ='outer', suffixes=('_1', '_2'))

# define custom function to adjust quantity
def adjust_quantity(row):
    # get quantities from merged dataframe
    q1 = row['quantity_1']
    q2 = row['quantity_2']
    
    # adjust quantity based on values in both dataframes
    if pd.isna(q2):
        return q1  # use quantity from df1 if not present in df2
    else:
        return q1 - q2  # subtract quantity of df2 from quantity in df1

# apply custom function to calculate adjusted quantity
merge_df['Quantity'] = merge_df.apply(adjust_quantity, axis=1)

# remove unnecessary columns and rename columns
merge_df.drop(['quantity_1', 'quantity_2', 'unit_2', 'category_2'], axis=1, inplace=True)
merge_df.rename(columns={'current items': 'Current items', 'unit_1':'Unit', 'category_1': 'Category'}, inplace=True)

merge_df


