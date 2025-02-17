import openai
import streamlit as st
import pyttsx3
from gtts import gTTS
from moviepy.editor import ImageClip, concatenate_videoclips
from PIL import Image
import requests
from io import BytesIO
from dotenv import load_dotenv
import os

# Load the .env file for your API keys and other sensitive info
load_dotenv()

# Set your OpenAI API key, Hygen API key, and 11 Labs API key
openai.api_key = os.getenv('OPENAI_API_KEY')  # Ensure you've set this in your .env file
HYGEN_API_KEY = os.getenv('HYGEN_API_KEY')  # Hygen API key
ELEVEN_LABS_API_KEY = os.getenv('ELEVEN_LABS_API_KEY')  # 11 Labs API key

# Function to generate text using OpenAI
def generate_text(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",  # Use the latest OpenAI model
        prompt=prompt,
        max_tokens=100
    )
    return response.choices[0].text.strip()

# Function to generate text using Hygen API (for example: script generation)
def generate_text_hygen(prompt):
    url = "https://api.hygen.com/v1/generate"  # Change to Hygen's actual endpoint if different
    headers = {
        'Authorization': f'Bearer {HYGEN_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {"prompt": prompt}
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json().get('text')
    else:
        return f"Error: {response.status_code}"

# Function to convert text to speech using pyttsx3
def text_to_speech_pyttsx3(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Function to convert text to speech using gTTS (Google TTS)
def text_to_speech_gtts(text):
    tts = gTTS(text)
    tts.save("output.mp3")
    os.system("start output.mp3")  # For Windows; use "mpg321 output.mp3" on Linux

# Function to convert text to speech using 11 Labs API (AI voice generation)
def text_to_speech_11labs(text):
    url = "https://api.elevenlabs.io/v1/speech"  # Change to 11 Labs' actual endpoint if different
    headers = {
        'Authorization': f'Bearer {ELEVEN_LABS_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        "text": text,
        "voice": "en_us_male",  # Specify the desired voice, this is an example
        "model": "elevenlabs-voice-model"  # Specify the voice model if required
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        with open("output_audio.wav", "wb") as f:
            f.write(response.content)
        os.system("start output_audio.wav")  # Play the audio file
    else:
        print(f"Error generating speech: {response.status_code}")

# Function to generate a video (if required)
def generate_video(image_url, output_filename="output_video.mp4"):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))

    # Create an ImageClip from the downloaded image
    clip = ImageClip(img)
    clip = clip.set_duration(5)  # 5 seconds duration for the clip
    clip.write_videofile(output_filename, fps=24)

# Streamlit app
st.title('AI Podcast Generator')

# User input for the prompt
prompt = st.text_input("Enter your prompt:")

if prompt:
    st.write("Generating response...")

    # Choose between OpenAI and Hygen for text generation
    use_hygen = st.checkbox("Use Hygen for text generation")  # Checkbox to select Hygen
    if use_hygen:
        generated_text = generate_text_hygen(prompt)
    else:
        generated_text = generate_text(prompt)

    st.write("Generated Text:")
    st.write(generated_text)

    # Text-to-speech conversion using 11 Labs (or fallback to gTTS)
    use_11labs = st.checkbox("Use 11 Labs for voice generation")  # Checkbox to select 11 Labs
    if use_11labs:
        text_to_speech_11labs(generated_text)
    else:
        text_to_speech_gtts(generated_text)

    # Optionally, create a video if required (add your image URL)
    # Uncomment the following line to generate a video
    # generate_video("https://your-image-url.com/image.jpg")
    
    st.write("Process complete!")
else:
    st.write("Please enter a prompt to generate text.")
