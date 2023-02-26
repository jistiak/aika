from dotenv import load_dotenv
import streamlit as st
import json
import pandas as pd
import redis
import os


st.set_page_config(page_title="What's in my Kitchen?", page_icon="🥘")

st.title("🥘 What's in my Kitchen?")

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
