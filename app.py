import random
from typing import List, Tuple
import streamlit as st
import pandas as pd
import psycopg2
from psycopg2 import sql

CSV_URL = "https://raw.githubusercontent.com/shkkonda/imageEloCalc/main/nokiamon_image.csv"
final_df = pd.read_csv(CSV_URL)

# Database connection details
host = 'database-1.cv9g4hhrgmvg.us-east-1.rds.amazonaws.com'
dbname = ''  # Update with your database name
user = 'postgres'
port = '5432'
password = 'wCJTQ205EKHWh6fXzxLc'

# Connect to the database
conn = psycopg2.connect(host=host, dbname=dbname, user=user, port=port, password=password)
cur = conn.cursor()

# Create user_selections table if it doesn't exist
cur.execute('''
    CREATE TABLE IF NOT EXISTS user_selections (
        id SERIAL PRIMARY KEY,
        left_image_link VARCHAR,
        right_image_link VARCHAR,
        selected_image_link VARCHAR,
        wallet_address VARCHAR,
        timestamp TIMESTAMP
    );
''')
conn.commit()

def get_random_image_pair(df) -> Tuple[str, str]:
    left_image = random.choice(df['image_link'])
    right_image = random.choice(df['image_link'])

    while left_image == right_image:
        right_image = random.choice(df['image_link'])

    return left_image, right_image

def show_image_pair(left_image: str, right_image: str, df):
    col1, col2 = st.columns(2)
    
    with col1:
        st.image(left_image, width=300)

    with col2:
        st.image(right_image, width=300)

    col3, col4 = st.columns(2)
    
    with col3:
        if st.button(label=df.loc[df['image_link'] == left_image, 'name'].iloc[0], key='left_button'):
            left_image, right_image = get_random_image_pair(df)
            show_image_pair(left_image, right_image, df)
            store_user_selection(left_image, right_image, left_image, wallet_address)

    with col4:
        if st.button(label=df.loc[df['image_link'] == right_image, 'name'].iloc[0], key='right_button'):
            left_image, right_image = get_random_image_pair(df)
            show_image_pair(left_image, right_image, df)
            store_user_selection(left_image, right_image, right_image, wallet_address)

def store_user_selection(left_image: str, right_image: str, selected_image: str, wallet_address: str):
    # Insert user selection into the user_selections table
    insert_query = sql.SQL('''
        INSERT INTO user_selections (left_image_link, right_image_link, selected_image_link, wallet_address, timestamp)
        VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP);
    ''')
    cur.execute(insert_query, (left_image, right_image, selected_image, wallet_address))
    conn.commit()

def main(df):
    st.title("Nokiamon ELO Rating")

    wallet_address = st.text_input("Wallet Address")

    left_image, right_image = get_random_image_pair(df)

    show_image_pair(left_image, right_image, df)

    # Store user selections and wallet addresses in the database
    store_user_selection(left_image, right_image, None, wallet_address)

    # You can enhance this implementation by adding user authentication,
    # tracking user selections, and calculating
