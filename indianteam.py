import streamlit as st
import requests
import pandas as pd

# Set Page Configuration
st.set_page_config(page_title="Indian Cricket Team", layout="wide")

# Free API Key (Replace if needed)
API_KEY = "INSERT_YOUR_FREE_API_KEY_HERE"  # Replace with your API key
BASE_URL = "https://api.cricapi.com/v1/"

# Sidebar Navigation
st.sidebar.title("🏏 Indian Cricket Dashboard")
page = st.sidebar.radio("Navigate to:", ["Home", "Trophies", "Player Stats", "Live Match Scores"])

# Home Page
if page == "Home":
    st.markdown(
        """
        <style>
            .home-container {
                background-image: url('INSERT_IMAGE_PATH_HERE'); 
                background-size: cover;
                padding: 50px;
                color: white;
                text-align: center;
            }
            .content {
                background-color: rgba(0, 0, 0, 0.7);
                padding: 20px;
                border-radius: 10px;
                display: inline-block;
            }
        </style>
        <div class="home-container">
            <div class="content">
                <h1>🇮🇳 Indian Cricket Team</h1>
                <p>
                    The Indian cricket team, also known as Team India, is one of the most successful teams in world cricket. 
                    India has won multiple ICC trophies, including the ICC Cricket World Cup, T20 World Cup, and Champions Trophy. 
                    With legendary players like Sachin Tendulkar, MS Dhoni, Virat Kohli, and Rohit Sharma, India has dominated the cricketing world for decades.
                    The team has a rich history of producing world-class batsmen, bowlers, and all-rounders.
                </p>
                <p>
                    India plays in all three formats – Tests, One Day Internationals (ODIs), and T20s. 
                    The team is known for its passionate fanbase and electrifying performances in home and away matches.
                </p>
                <p>
                    The Board of Control for Cricket in India (BCCI) governs the Indian team and organizes tournaments such as the Indian Premier League (IPL).
                    India’s cricket journey continues to inspire millions of aspiring cricketers around the world.
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Trophies Page
elif page == "Trophies":
    st.title("🏆 ICC Trophies Won by India")
    trophies = {
        "🏆 ICC Cricket World Cup (1983, 2011)": "INSERT_IMAGE_PATH_HERE",
        "🏆 ICC T20 World Cup (2007)": "INSERT_IMAGE_PATH_HERE",
        "🏆 ICC Champions Trophy (2002, 2013)": "INSERT_IMAGE_PATH_HERE",
        "🏆 ICC Test Mace (2010, 2011, 2017)": "INSERT_IMAGE_PATH_HERE",
    }
    
    for trophy, image in trophies.items():
        st.markdown(f"### {trophy}")
        st.image(image, caption=trophy)  # Replace with actual image paths

# Player Stats Page
elif page == "Player Stats":
    st.title("📊 Player Statistics")
    player_name = st.text_input("Enter Player Name", "Virat Kohli")
    
    if st.button("Get Stats"):
        response = requests.get(f"{BASE_URL}players?apikey={API_KEY}&name={player_name}")
        if response.status_code == 200:
            data = response.json()
            if data["status"] == "success" and "data" in data and data["data"]:
                player = data["data"][0]  # Taking the first result
                st.write(f"### {player['name']}")
                
                stats = {
                    "Matches": player.get("matches", "N/A"),
                    "Runs": player.get("runs", "N/A"),
                    "Wickets": player.get("wickets", "N/A"),
                    "Batting Average": player.get("battingAverage", "N/A"),
                    "Bowling Average": player.get("bowlingAverage", "N/A"),
                }
                
                df = pd.DataFrame(stats.items(), columns=["Stat", "Value"])
                st.table(df)
            else:
                st.warning("Player not found or no data available.")
        else:
            st.error("Failed to fetch data. Please check the API key or try again later.")

# Live Match Scores Page
elif page == "Live Match Scores":
    st.title("🏏 Live Scorecard - Indian Team")
    
    response = requests.get(f"{BASE_URL}matches?apikey={API_KEY}")
    if response.status_code == 200:
        data = response.json()
        if data["status"] == "success" and "data" in data:
            matches = [match for match in data["data"] if "India" in match["teamInfo"][0]["name"] or "India" in match["teamInfo"][1]["name"]]
            
            if matches:
                for match in matches:
                    st.markdown(f"### {match['name']} - {match['matchType']}")  # Match title
                    st.write(f"📅 Date: {match['date']}")
                    st.write(f"🏟 Venue: {match['venue']}")
                    st.write(f"⏳ Status: {match['status']}")
                    
                    if "score" in match:
                        st.write(f"**{match['teamInfo'][0]['name']}** - {match['score'][0]['runs']}/{match['score'][0]['wickets']} in {match['score'][0]['overs']} overs")
                        st.write(f"**{match['teamInfo'][1]['name']}** - {match['score'][1]['runs']}/{match['score'][1]['wickets']} in {match['score'][1]['overs']} overs")
                    
                    st.write("---")  # Separator for multiple matches
            else:
                st.warning("No live matches featuring India at the moment.")
        else:
            st.warning("No match data available.")
    else:
        st.error("Failed to fetch match data. Please check the API key or try again later.")

