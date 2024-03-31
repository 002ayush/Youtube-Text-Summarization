import streamlit as st
from dotenv import load_dotenv
load_dotenv() #It will loaad all the environment variables
import google.generativeai as genai
import os
from youtube_transcript_api import YouTubeTranscriptApi
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
prompt = "You are giving the prompt here.The transcript will appended here...."
def extract_transcript_details(youtube_url):
    try:
        video_id = youtube_url.split("=")[1]
        trascript_text = YouTubeTranscriptApi.get_transcript(video_id,languages=['en','hi'])
        transcript = ""
        for i in trascript_text:
            transcript += " " + i["text"]
        return transcript
    except Exception as e:
        raise e
#This is only for summary based on Prompt from Google Gemini Pro
def generate_gemini_content(transcript_text,prompt):

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt+transcript_text)
    return response.text
#Creating a streamlit app
st.title("Youtube Transcript")
youtube_link = st.text_input("Enter the Youtube Video link")
if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg",use_column_width=True)
if st.button("Get Transcript"):
    transcript_text = extract_transcript_details(youtube_link)
    if transcript_text:
        summary = generate_gemini_content(transcript_text,prompt)
        st.markdown("##Detailed Notes")
        st.write(summary)
