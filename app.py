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

def show_image_pair(left_image: str, right_image: str):
    col1, col2 = st.beta_columns(2)
    with col1:
        st.image(left_image, width=300)
    with col2:
        st.image(right_image, width=300)

def main(df):
    st.title("Nokiamon ELO Rating")

    left_image, right_image = get_random_image_pair(df)

    show_image_pair(left_image, right_image)

    # You can enhance this implementation by adding user authentication,
    # tracking user selections, and calculating the ELO rating for each Nokiamon.
    # To do that, you'll need to store user selections and ELO ratings in a database.

if __name__ == "__main__":
    main(final_df)
