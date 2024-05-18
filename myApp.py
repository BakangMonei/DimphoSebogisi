import streamlit as st
import pandas as pd
import random
import plotly.express as px
import csv
import os
import requests
import pycountry
from datetime import datetime

# Function to log navigation events
def log_navigation(ip_address, country, page, main_interest, device, additional_info=""):
    log_entry = {
        "Country of origin": country,
        "Number of visits to the website": 1,  # Increment visits logic can be added
        "Time of each visit": datetime.now().isoformat(),
        "Main interest": main_interest,
        "Device used to access website": device,
        "IP address": ip_address
    }
    log_file = "my_web_logs.csv"
    
    # Check if the log file exists, if not create it with a header
    if not os.path.exists(log_file):
        with open(log_file, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=log_entry.keys())
            writer.writeheader()
    
    # Append the log entry to the file
    with open(log_file, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=log_entry.keys())
        writer.writerow(log_entry)

# Function to get the user's IP address
def get_user_ip():
    try:
        response = requests.get("https://httpbin.org/ip")
        return response.json()["origin"]
    except requests.RequestException:
        return "unknown"

# Function to get the user's country based on IP address
def get_user_country(ip_address):
    try:
        response = requests.get(f"https://ipapi.co/{ip_address}/json/")
        country_name = response.json().get("country_name", "unknown")
        return country_name
    except requests.RequestException:
        return "unknown"

# Inject JavaScript to get browser details
get_browser_details = """
<script>
    function getBrowserInfo() {
        var userAgent = navigator.userAgent;
        var browserName = "Unknown";
        if (userAgent.indexOf("Firefox") > -1) {
            browserName = "Mozilla Firefox";
        } else if (userAgent.indexOf("SamsungBrowser") > -1) {
            browserName = "Samsung Internet";
        } else if (userAgent.indexOf("Opera") > -1 || userAgent.indexOf("OPR") > -1) {
            browserName = "Opera";
        } else if (userAgent.indexOf("Trident") > -1) {
            browserName = "Microsoft Internet Explorer";
        } else if (userAgent.indexOf("Edge") > -1) {
            browserName = "Microsoft Edge";
        } else if (userAgent.indexOf("Chrome") > -1) {
            browserName = "Google Chrome";
        } else if (userAgent.indexOf("Safari") > -1) {
            browserName = "Safari";
        }
        else if (userAgent.indexOf("Brave") > -1) {
            browserName = "Brave";
        }
        return browserName;
    }
    const browserInfo = getBrowserInfo();
    const browserElement = document.createElement("div");
    browserElement.id = "browser-info";
    browserElement.style.display = "none";
    browserElement.textContent = browserInfo;
    document.body.appendChild(browserElement);
</script>
"""

st.markdown(get_browser_details, unsafe_allow_html=True)

# Function to get browser details
def get_browser_info():
    return st.query_params.get("browser-info", ["unknown"])[0]

# Get user's IP address and country
ip_address = get_user_ip()
country = get_user_country(ip_address)

# Define the data attributes
ATTRIBUTES = [
    "Username",
    "Password"
]

# Define the login, logout and registration functions
def login(username, password):
    # Read usernames and passwords from CSV file
    df = pd.read_csv("user_credentials.csv")
    if (df['Username'] == username).any() and (df[df['Username'] == username]['Password'].iloc[0] == password):
        st.session_state['logged_in'] = True
        st.session_state['username'] = username
        return True
    return False

def register(username, password):
    # Append new registration to the CSV file
    new_data = pd.DataFrame({'Username': [username], 'Password': [password]})
    with open("user_credentials.csv", "a") as file:
        new_data.to_csv(file, header=False, index=False)
    return True

def logout():
    st.session_state['logged_in'] = False
    st.session_state['username'] = ""

# Function to generate data
@st.cache_data
def generate_data(n_rows):
    data = []
    for _ in range(n_rows):
        row = {
            "Timestamps": datetime.now().isoformat(),
            "IP address": get_user_ip(),
            "Country": random.choice([country.name for country in pycountry.countries]),
            "Athlete names": f"Athlete_{random.randint(1, 100)}",
            "Sports": random.choice(["Swimming", "Athletics", "Gymnastics", "Soccer", "Tennis"]),
            "Age": random.randint(18, 40),
            "Gender": random.choice(["Male", "Female"]),
            "Nationality": random.choice([country.name for country in pycountry.countries]),
            "Match or sport event dates": datetime.now().isoformat(),
            "Outcomes": random.choice(["Win", "Lose", "Draw"]),
            "Medals": random.choice(["Gold", "Silver", "Bronze", "None"]),
            "Ranks": random.randint(1, 10),
            "Stadiums": random.choice(["Stadium A", "Stadium B", "Stadium C"]),
            "Athlete Height": random.uniform(1.5, 2.0),
            "Athlete weight": random.uniform(50, 100),
            "Date of competition": datetime.now().isoformat()
        }
        data.append(row)
    return pd.DataFrame(data)

data = generate_data(100)

# Create the Streamlit app
st.title("Analytical Tool")

# Create the sidebar
st.sidebar.title("Navigation")
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['username'] = ""

if st.session_state['logged_in']:
    pages = ["Dashboard", "Upload CSV", "Feedback", "Logout"]
else:
    pages = ["Login", "Register"]

page = st.sidebar.selectbox("Select a page", pages)

# Log navigation to the selected page
main_interest = "Sports Analytics"
device = get_browser_info()
log_navigation(ip_address, country, page, main_interest, device)

if page == "Login":
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if login(username, password):
            st.success("Login successful!")
            st.query_params = {"page": "Dashboard"}  # Automatically switch to dashboard after successful login
        else:
            st.error("Invalid credentials")

elif page == "Register":
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        if register(username, password):
            st.success("Registration successful!")
        else:
            st.error("Registration failed")

elif page == "Logout":
    logout()
    st.success("Logged out successfully!")
    st.query_params = {"page": "Login"}

elif page == "Dashboard":
    # Create the dashboard
    st.header("Dashboard")
    sport_of_interest = st.selectbox("Select a sport", ["Swimming", "Athletics", "Gymnastics", "Soccer", "Tennis"])
    continent = st.selectbox("Select a continent", ["Asia", "Europe", "Africa", "North America", "South America"])
    country = st.selectbox("Select a country", [country.name for country in pycountry.countries])

    # Create the visualizations
    fig = px.bar(data, x="Country", y="Ranks", color="Sports", barmode="group")
    st.plotly_chart(fig)

    fig = px.pie(data, names="Country", values="Ranks")
    st.plotly_chart(fig)

    # Create the report views
    st.header("Reports")
    report_type = st.selectbox("Select a report type", ["Games played in a day", "Most played sport per country", "Most played sport per gender and country"])
    analysis_results = None
    if report_type == "Games played in a day":
        analysis_results = data.groupby("Country").size()
        st.write(analysis_results)
    elif report_type == "Most played sport per country":
        analysis_results = data.groupby(["Country", "Sports"]).size()
        st.write(analysis_results)
    elif report_type == "Most played sport per gender and country":
        analysis_results = data.groupby(["Country", "Gender", "Sports"]).size()
        st.write(analysis_results)
    
    # Save analysis results to CSV
    if analysis_results is not None:
        analysis_results.to_csv("analysis.csv")

elif page == "Upload CSV":
    # Create the CSV upload functionality
    st.header("Upload CSV")
    uploaded_file = st.file_uploader("Select a CSV file", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write(df.head())

elif page == "Feedback":
    st.header("User Feedback")
    st.write("Please provide your feedback:")
    feedback_text = st.text_area
