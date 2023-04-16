import os
import random
import streamlit as st
import pandas as pd
from streamlit_image_select import image_select

IMAGE_FOLDER = "nokiamon_list/"
CSV_URL = "https://raw.githubusercontent.com/shkkonda/imageEloCalc/main/responses.csv"

def get_random_images():
    images = os.listdir(IMAGE_FOLDER)
    image1 = random.choice(images)
    image2 = random.choice(images)
    while image1 == image2:
        image2 = random.choice(images)
    return image1, image2

def main():
    st.set_page_config(page_title="Image Preference Survey")

    st.title("Image Preference Survey")
    st.write("Please select which image you prefer out of the two options shown.")

    image1, image2 = get_random_images()

    selected_image = image_select([os.path.join(IMAGE_FOLDER, image1), os.path.join(IMAGE_FOLDER, image2)])
    if selected_image:
        # Store the response in a CSV file on GitHub
        data = {"Image 1": os.path.join(IMAGE_FOLDER, image1), "Image 2": os.path.join(IMAGE_FOLDER, image2), "Choice": selected_image}
        df = pd.DataFrame(data, index=[0])
        filename = "responses.csv"
        try:
            df_existing = pd.read_csv(CSV_URL)
            df_existing = pd.concat([df_existing, df], ignore_index=True)
            df_existing.to_csv(filename, index=False)
            st.success("Response submitted successfully.")
        except Exception as e:
            st.error("Failed to submit response. Error: " + str(e))

if __name__ == "__main__":
    main()
