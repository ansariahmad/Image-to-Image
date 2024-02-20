from clarifai.modules.css import ClarifaiStreamlitCSS
from clarifai.client.model import Model
from clarifai.client.input import Inputs
import streamlit as st
import requests
from io import BytesIO
import base64
import os
from PIL import Image
from os import listdir
from os.path import splitext
from assistant import generate_prompt

st.set_page_config(layout="wide")
ClarifaiStreamlitCSS.insert_default_css(st)

# Function to call the image to image conversion API
def convert_image(openai_key, image):
    model_url = "https://clarifai.com/openai/chat-completion/models/openai-gpt-4-vision"
    prompt = "Explain the beauty in the image."

    inference_params = dict(temperature=0.2, max_tokens=100)
    model_prediction = Model(model_url).predict(inputs =
                                                [Inputs.get_multimodal_input(input_id="",
                                                                            image_bytes = image,
                                                                            raw_text=prompt)],
                                                inference_params=inference_params)

    image_description = model_prediction.outputs[0].data.text.raw
    image_prompt = generate_prompt(openai_key, image_description)
    inference_params = dict(quality="standard", size= '1024x1024')

    # Model Predict
    model_prediction = Model("https://clarifai.com/openai/dall-e/models/dall-e-3").predict_by_bytes(image_prompt.encode(), input_type="text", inference_params=inference_params)

    output_base64 = model_prediction.outputs[0].data.image.base64

    # output_image = image  # Placeholder for demonstration purpose
    return output_base64

# Streamlit app
def main():
    st.title("Image to Image")

    # Input API Key from user
    clarifai_pat = st.text_input("Enter CLARIFAI PAT")
    openai_key = st.text_input("Enter OpenAI KEY")
    os.environ['CLARIFAI_PAT'] = clarifai_pat

    # Upload image
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Check if the uploaded file is an image
        if uploaded_file.type.split('/')[0] == 'image':
            image = Image.open(uploaded_file)
            st.image(image, caption='Uploaded Image', use_column_width=True)

            # Convert image using API
            output_image = convert_image(openai_key, uploaded_file.getvalue())
            # output_image = BytesIO(base64.b64decode(output_image))
            output_image = Image.open(BytesIO(output_image))

            st.image(output_image, caption='Converted Image', use_column_width=True)
            # st.write(output_image)
        else:
            st.error("Error: Please upload an image file.")

if __name__ == "__main__":
    main()
