import random
from typing import List, Tuple
import streamlit as st
import pandas as pd

CSV_URL = "https://raw.githubusercontent.com/shkkonda/imageEloCalc/main/nokiamon_image.csv"
final_df = pd.read_csv(CSV_URL)

def get_random_image_pair(df) -> Tuple[str, str]:
    left_image = random.choice(df['image_link'])
    right_image = random.choice(df['image_link'])

    while left_image == right_image:
        right_image = random.choice(df['image_link'])

    return left_image, right_image

def show_image_pair(left_image: str, right_image: str, df):
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(label=df.loc[df['image_link'] == left_image, 'name'].iloc[0], key='left_button'):
            left_image, right_image = get_random_image_pair(df)
            show_image_pair(left_image, right_image, df)
        st.image(left_image, width=300)

    with col2:
        if st.button(label=df.loc[df['image_link'] == right_image, 'name'].iloc[0], key='right_button'):
            left_image, right_image = get_random_image_pair(df)
            show_image_pair(left_image, right_image, df)
        st.image(right_image, width=300)

def main(df):
    st.title("Nokiamon ELO Rating")

    wallet_address = st.text_input("Wallet Address")

    left_image, right_image = get_random_image_pair(df)

    show_image_pair(left_image, right_image, df)

    # Store user selections and wallet addresses in a database
    # store_user_selection(left_image, right_image, wallet_address)

    # You can enhance this implementation by adding user authentication,
    # tracking user selections, and calculating the ELO rating for each Nokiamon.
    # To do that, you'll need to store user selections and ELO ratings in a database.

if __name__ == "__main__":
    main(final_df)
