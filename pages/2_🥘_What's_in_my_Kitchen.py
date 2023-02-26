import streamlit as st
import json
import pandas as pd
import redis
import os


st.set_page_config(page_title="What's in my Kitchen?", page_icon="🥘")

st.title("🥘 What's in my Kitchen?")

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


data = redis_call(r_host, r_port, r_pass)

st.text(data)

# df = pd.DataFrame()

# for i in range(len(data)):
#     for key, value in data[i].items():
#         temp_df = pd.DataFrame.from_dict(value, orient='index').T
#         temp_df.index = [key]
#         df = pd.concat([df, temp_df])

# st.dataframe(df)
