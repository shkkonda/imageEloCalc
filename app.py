import random
from typing import List, Tuple
import streamlit as st
import pandas as pd
import psycopg2
from psycopg2 import sql

CSV_URL = "https://raw.githubusercontent.com/shkkonda/imageEloCalc/main/nokiamon_image.csv"
final_df = pd.read_csv(CSV_URL)

# Create a singleton object for the database connection
@st.cache_resource
def get_database_connection():
    conn = psycopg2.connect(
        host="database-1.cv9g4hhrgmvg.us-east-1.rds.amazonaws.com",
        user="postgres",
        password="eRYebFlJePOFRZeVVuQT",
        database=""
    )
    return conn

# Perform query.
def store_user_selection(conn, left_image: str, right_image: str, selected_image: str, wallet_address: str):
    # Insert user selection into the user_selections table
    insert_query = sql.SQL('''
        INSERT INTO user_selections (left_image_link, right_image_link, selected_image_link, wallet_address, timestamp)
        VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP);
    ''')
    
    cursor = get_database_connection().cursor()
    cursor.execute(insert_query, (left_image, right_image, selected_image, wallet_address))
    get_database_connection().commit()
    st.write("Data saved to database!")

def get_random_image_pair(df) -> Tuple[str, str]:
    left_image = random.choice(df['image_link'])
    right_image = random.choice(df['image_link'])

    while left_image == right_image:
        right_image = random.choice(df['image_link'])

    return left_image, right_image

def show_image_pair(left_image: str, right_image: str, df, wallet_address: str):
    col1, col2 = st.columns(2)
    
    with col1:
        st.image(left_image, width=300)

    with col2:
        st.image(right_image, width=300)

    col3, col4 = st.columns(2)
    
    with col3:
        if st.button(label=df.loc[df['image_link'] == left_image, 'name'].iloc[0], key=f'left_button_{left_image}'):
            print("Hope it gets printed")
            store_user_selection(conn, left_image, right_image, left_image, wallet_address)

    with col4:
        if st.button(label=df.loc[df['image_link'] == right_image, 'name'].iloc[0], key=f'right_button_{right_image}'):
            store_user_selection(conn, left_image, right_image, right_image, wallet_address)

def main(df):
    st.title("Nokiamon ELO Rating")

    wallet_address = st.text_input("Wallet Address")

    left_image, right_image = get_random_image_pair(df)

    show_image_pair(left_image, right_image, df, wallet_address)

if __name__ == "__main__":
    main(final_df)
