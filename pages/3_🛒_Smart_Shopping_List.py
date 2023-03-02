from dotenv import load_dotenv
import streamlit as st
import json
import pandas as pd
import redis
import os


st.set_page_config(page_title="Smart Shopping List", page_icon="🛒")


st.title("🛒 Smart Shopping List")

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


df = redis2df(data)



# Load the existing index set from a text file
try:
    with open('assets/grocery_set.txt', 'r') as f:
        index_set = set([line.strip().lower() for line in f])
except FileNotFoundError:
    index_set = set()

# Add new items to the index set
new_items = set(df.index) - index_set
index_set.update(new_items)

# Save the updated index set to a text file
with open('assets/grocery_set.txt', 'w') as f:
    for item in index_set:
        f.write(str(item).lower() + '\n')

# Check for missing items and generate a markdown checklist
missing_items = []
for item in index_set:
    for idx in df.index:
        if item != idx.lower():
            missing_items.append(item)

missing_items = list(set(missing_items))

if missing_items:
    st.subheader("Items to buy:")
    for item in missing_items:
        st.markdown(f" - [ ] {item.title()}")
else:
    st.markdown("No items to buy.")
