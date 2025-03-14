import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(page_title='Indian Cricket Live Updates', layout='wide')

# RapidAPI Configuration
RAPIDAPI_KEY = "cb77671a24msh0dc75b4dba7ae7dp1ce346jsndd7b9cf9d9ff"
RAPIDAPI_HOST = "cricbuzz-cricket.p.rapidapi.com"
BASE_URL = "https://cricbuzz-cricket.p.rapidapi.com/"

# Headers for API Requests
HEADERS = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": RAPIDAPI_HOST
}

# Custom CSS for styling
st.markdown("""
    <style>
        body {
            background-color: #ffffff;
        }
        .main-title {
            text-align: center;
            font-size: 36px;
            color: #1e90ff;
            font-weight: bold;
        }
        .sub-title {
            font-size: 24px;
            color: #1e90ff;
        }
        .highlight {
            background-color: #1e90ff;
            padding: 10px;
            border-radius: 10px;
            color: white;
            text-align: center;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("🏏 Indian Cricket Dashboard")
page = st.sidebar.radio("Select a page", ["Live Updates", "Player Stats", "Achievements", "Top Performers"])

# Live Updates Page
def live_updates():
    st.markdown("<h1 class='main-title'>Live Match Updates</h1>", unsafe_allow_html=True)
    
    # Fetch Live Matches
    response = requests.get(f"{BASE_URL}matches/v1/recent", headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        if 'matchList' in data:
            matches = [match for match in data['matchList'] if "India" in match.get('team1', {}).get('teamName', '') or "India" in match.get('team2', {}).get('teamName', '')]
            if matches:
                for match in matches:
                    st.markdown(f"**{match['seriesName']} - {match['matchDesc']}**")
                    st.write(f"Status: {match.get('status', 'Unknown')}")
                    st.write(f"Teams: {match.get('team1', {}).get('teamName', 'N/A')} vs {match.get('team2', {}).get('teamName', 'N/A')}")
                    st.write("---")
            else:
                st.warning("No live matches found for India.")
        else:
            st.error("Invalid data format received.")
    else:
        st.error("Failed to fetch live updates. Try again later.")

# Player Stats Page
def player_stats():
    st.markdown("<h1 class='main-title'>Player Statistics</h1>", unsafe_allow_html=True)
    
    player_name = st.text_input("Enter Player Name", "Virat Kohli")
    if st.button("Get Stats"):
        response = requests.get(f"{BASE_URL}stats/v1/player?name={player_name}", headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            if 'careerSummary' in data:
                player = data
                st.write(f"### {player['name']}")
                stats = {
                    "Matches": player.get("matches", "N/A"),
                    "Runs": player.get("runs", "N/A"),
                    "Wickets": player.get("wickets", "N/A"),
                    "Average": player.get("average", "N/A")
                }
                df = pd.DataFrame(stats.items(), columns=["Stat", "Value"])
                st.table(df)
                
                # Generate graph for player's performance
                years = list(range(2010, 2024))  # Example years
                runs = [player.get("runs", 0) // len(years) for _ in years]  # Sample data
                wickets = [player.get("wickets", 0) // len(years) for _ in years]  # Sample data
                
                fig, ax = plt.subplots()
                ax.plot(years, runs, label="Runs", marker="o")
                ax.plot(years, wickets, label="Wickets", marker="s", linestyle="dashed")
                ax.set_xlabel("Year")
                ax.set_ylabel("Performance")
                ax.set_title(f"Performance Analysis of {player_name}")
                ax.legend()
                st.pyplot(fig)
            else:
                st.warning("Player not found.")
        else:
            st.error("Failed to fetch player stats. Check API response.")

# Achievements Page
def achievements():
    st.markdown("<h1 class='main-title'>Team Achievements</h1>", unsafe_allow_html=True)
    achievements = ["ICC Cricket World Cup - 1983, 2011", "ICC T20 World Cup - 2007", "Champions Trophy - 2002, 2013"]
    for trophy in achievements:
        st.markdown(f"<div class='highlight'>{trophy}</div>", unsafe_allow_html=True)
    
    # Image placeholder (Replace path with actual image path)
    st.image("path_to_trophy_image.jpg", caption="Team India's Achievements")

# Top Performers Page
def top_performers():
    st.markdown("<h1 class='main-title'>Top Performers</h1>", unsafe_allow_html=True)
    
    data = {"Player": ["Virat Kohli", "Rohit Sharma", "Jasprit Bumrah"], "Performance": ["1200 Runs", "1000 Runs", "50 Wickets"]}
    df = pd.DataFrame(data)
    st.table(df)
    
    # Image placeholder (Replace path with actual image path)
    st.image("path_to_top_performers.jpg", caption="Top Performers of India")

# Routing Pages
if page == "Live Updates":
    live_updates()
elif page == "Player Stats":
    player_stats()
elif page == "Achievements":
    achievements()
elif page == "Top Performers":
    top_performers()


