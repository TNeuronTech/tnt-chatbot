import os
import streamlit as st
import re
from modules.layout import Layout
from modules.utils import Utilities
from modules.utils import DataType
from modules.sidebar import Sidebar

from modules.restclient import restClient

st.set_page_config(layout="wide", page_icon="💬", page_title="Chatbot 🤖")

# Instantiate the main components
layout, sidebar, utils = Layout(), Sidebar(), Utilities()

st.markdown(
    f"""
    <h1 style='text-align: center;'> Ask chatbot to summarize youtube video ! 😁</h1>
    """,
    unsafe_allow_html=True,
)

user_api_key = utils.load_api_key()

sidebar.about()

if not user_api_key:
    layout.show_api_key_missing()

else:
    os.environ["OPENAI_API_KEY"] = user_api_key

    script_docs = []

    def get_youtube_id(url):
        video_id = None
        match = re.search(r"(?<=v=)[^&#]+", url)
        if match :
            video_id = match.group()
        else : 
            match = re.search(r"(?<=youtu.be/)[^&#]+", url)
            if match :
                video_id = match.group()
        return video_id

    video_url = st.text_input(placeholder="Enter Youtube Video URL", label_visibility="hidden", label =" ")
    if video_url :
        video_id = get_youtube_id(video_url)
        if video_id != "":
            
            with st.spinner("Processing..."):
                result = restClient.summerize_video(
                    user_api_key,
                    video_id,
                    DataType.VIDEO)

            if result['status']:
                st.subheader(result['data']['result'])
            else:
                st.error(f"Error: {result['data']['detail']}")
            
