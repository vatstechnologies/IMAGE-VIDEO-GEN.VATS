import openai
import streamlit as st
import requests
import os
from dotenv import load_dotenv
from moviepy.editor import ImageClip, concatenate_videoclips
from PIL import Image
import pyttsx3
import gtts
import time

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to generate text
def generate_text(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

# Function to generate images
def generate_image(prompt):
    response = openai.images.generate(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    return response.data[0].url

# Streamlit UI
st.title("VatsGenix AI Podcast Generator 🎙️")

prompt = st.text_input("Enter your prompt:")

if st.button("Generate Text"):
    if prompt:
        text_output = generate_text(prompt)
        st.write(text_output)

if st.button("Generate Image"):
    if prompt:
        image_url = generate_image(prompt)
        st.image(image_url, caption="Generated Image")

