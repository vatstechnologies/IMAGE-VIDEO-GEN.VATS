import openai
import os
import pyttsx3
import streamlit as st
from gtts import gTTS
#from moviepy.editor import *   If you're not using moviepy, remove this line
from PIL import Image
import requests
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

# OpenAI API key from environment
openai.api_key = os.getenv('OPENAI_API_KEY')

# Streamlit page config
st.set_page_config(page_title="VatsGenixAI -  Podcast Generator", page_icon=":guardsman:", layout="wide")

# Sidebar setup
st.sidebar.title("Settings")
prompt = st.sidebar.text_input("Enter prompt:", "Describe a fascinating AI story")

# Function to generate text from OpenAI API
def generate_text(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7
    )
    return response.choices[0].text.strip()

# Function to convert text to speech using gTTS
def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    tts.save("audio.mp3")
    return "audio.mp3"

# Function to display the image
def generate_image(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    image_url = response['data'][0]['url']
    img = Image.open(requests.get(image_url, stream=True).raw)
    return img

# Function to play audio
def play_audio():
    audio_file = open("audio.mp3", "rb")
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format="audio/mp3")

# Main function
def main():
    st.title("AI Podcast Generator")

    if prompt:
        # Generate text from OpenAI API
        generated_text = generate_text(prompt)
        st.subheader("Generated Text:")
        st.write(generated_text)

        # Convert text to speech and play audio
        audio_path = text_to_speech(generated_text)
        st.subheader("Audio Output:")
        play_audio()

        # Generate and display image
        image = generate_image(prompt)
        st.subheader("Generated Image:")
        st.image(image)

if __name__ == "__main__":
    main()
