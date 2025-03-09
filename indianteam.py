import streamlit as st
import requests
import json
import time
from streamlit_lottie import st_lottie
from PIL import Image
import base64

# Load Lottie Animations
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Set Page Config
st.set_page_config(page_title="Indian Cricket Showcase", page_icon="🏏", layout="wide")

# Load Background CSS with Particle Effects
page_bg = f'''
<style>
[data-testid="stAppViewContainer"] {{
    background: url("https://wallpaperaccess.com/full/2078822.jpg") no-repeat center center fixed;
    background-size: cover;
}}
</style>
'''
st.markdown(page_bg, unsafe_allow_html=True)

# Title and Description
st.markdown("<h1 style='text-align: center; color: white;'>🇮🇳 Indian Cricket Showcase 🏏</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: white;'>A Tribute to India's Cricketing Legacy from 1983 Onwards</p>", unsafe_allow_html=True)

# Load Trophy Images
def display_trophy(image_path, title):
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.image(image_path, caption=title, use_column_width=True)

def display_player(image_path, name, description):
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(image_path, width=150)
    with col2:
        st.markdown(f"### {name}")
        st.write(description)

# Section 1: Trophies Won by India
st.markdown("## 🏆 Trophies Won by India")

display_trophy("images/1983_wc.jpg", "🏆 1983 Cricket World Cup")
display_trophy("images/2007_t20.jpg", "🏆 2007 ICC T20 World Cup")
display_trophy("images/2011_wc.jpg", "🏆 2011 Cricket World Cup")
display_trophy("images/2013_ct.jpg", "🏆 2013 ICC Champions Trophy")

# Section 2: Legendary Players
st.markdown("## 🌟 Legendary Performers")

display_player("images/sachin.jpg", "Sachin Tendulkar", "The 'God of Cricket' and India's highest run-scorer in history.")
display_player("images/dhoni.jpg", "MS Dhoni", "Captain Cool who led India to 3 ICC titles including the 2011 World Cup.")
display_player("images/kohli.jpg", "Virat Kohli", "One of the best modern-day batsmen with immense passion and records.")
display_player("images/yuvraj.jpg", "Yuvraj Singh", "Hero of the 2011 World Cup, famous for hitting 6 sixes in an over.")

time.sleep(1)
st.success("Enjoy exploring Indian Cricket's journey! 🏏")
