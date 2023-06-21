import random
from typing import List, Tuple
import streamlit as st
import pandas as pd

CSV_URL = "https://raw.githubusercontent.com/shkkonda/imageEloCalc/main/nokiamon_image.csv"
final_df = pd.read_csv(CSV_URL)

selected_data = []

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

    if st.button(label=df.loc[df['image_link'] == left_image, 'name'].iloc[0], key=f'left_button_{left_image}'):
        left_image, right_image = get_random_image_pair(df)
        store_user_selection(left_image, right_image, left_image, wallet_address)
        show_image_pair(left_image, right_image, df, wallet_address)

    if st.button(label=df.loc[df['image_link'] == right_image, 'name'].iloc[0], key=f'right_button_{right_image}'):
        left_image, right_image = get_random_image_pair(df)
        store_user_selection(left_image, right_image, right_image, wallet_address)
        show_image_pair(left_image, right_image, df, wallet_address)

def store_user_selection(left_image: str, right_image: str, selected_image: str, wallet_address: str):
    selected_data.append({
        'Left Image': left_image,
        'Right Image': right_image,
        'Selected Image': selected_image,
        'Wallet Address': wallet_address,
    })

def display_stored_selections():
    if selected_data:
        df = pd.DataFrame(selected_data)
        st.subheader("Stored Selections")
        st.dataframe(df)
    else:
        st.write("No stored selections yet.")

def main(df):
    st.title("Nokiamon ELO Rating")

    wallet_address = st.text_input("Wallet Address")

    left_image, right_image = get_random_image_pair(df)

    show_image_pair(left_image, right_image, df, wallet_address)
    display_stored_selections()

if __name__ == "__main__":
    main(final_df)
