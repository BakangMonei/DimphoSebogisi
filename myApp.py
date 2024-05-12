import csv
import passlib.hash
import streamlit as st
import pandas as pd
import random
import plotly.express as px
from plotly.graph_objs import Figure
import time
import socket
from urllib.parse import urlparse

# Define the data attributes
ATTRIBUTES = [
    "Timestamp",
    "IP_Address",
    "Country",
    "AthleteNames",
    "Sports",
    "Age",
    "Gender",
    "Nationality",
    "Match_or_sport_event_dates",
    "Outcomes",
    "Medals",
    "Ranks",
    "Stadiums",
    "Athlete_Height",
    "Athlete_Weight",
    "Date_of_Birth"
]

# Define the data generation function
def generate_data(n_rows):
    data = []
    for _ in range(n_rows):
        row = {
            "Timestamp": pd.Timestamp.now(),
            "IP_Address": f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
            "Country": random.choice(["USA", "China", "India", "Russia", "Germany"]),
            "AthleteNames": random.choice(["Michael Phelps", "Usain Bolt", "Simone Biles", "Lionel Messi", "Serena Williams"]),
            "Sports": random.choice(["Swimming", "Athletics", "Gymnastics", "Soccer", "Tennis"]),
            "Age": random.randint(18, 40),
            "Gender": random.choice(["Male", "Female"]),
            "Nationality": random.choice(["USA", "China", "India", "Russia", "Germany"]),
            "Match_or_sport_event_dates": pd.Timestamp.now(),
            "Outcomes": random.choice(["Win", "Lose", "Draw"]),
            "Medals": random.choice(["Gold", "Silver", "Bronze", ""]),
            "Ranks": random.randint(1, 10),
            "Stadiums": random.choice(["Olympic Stadium", "Wembley Stadium", "Madison Square Garden", "Bird's Nest"]),
            "Athlete_Height": random.randint(150, 220),
            "Athlete_Weight": random.randint(50, 150),
            "Date_of_Birth": pd.Timestamp.now() - pd.DateOffset(years=random.randint(18, 40))
        }
        data.append(row)
    return pd.DataFrame(data)

# Define the login and registration functions
def load_credentials():
    credentials = []
    with open('credentials.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            credentials.append(row)
    return {row[0]: row[1] for row in credentials}

def hash_password(password):
    return passlib.hash.pbkdf2_sha256.hash(password)

def verify_password(password, hashed_password):
    return passlib.hash.pbkdf2_sha256.verify(password, hashed_password)

def login(username, password):
    credentials = load_credentials()
    if username in credentials:
        stored_password = credentials[username]
        if verify_password(password, stored_password):
            return True
    return False

def register(username, password):
    credentials = load_credentials()
    if username not in credentials:
        hashed_password = hash_password(password)
        credentials.append([username, hashed_password])
        with open('credentials.csv', 'w') as f:
            writer = csv.writer(f)
            for cred in credentials:
                writer.writerow(cred)
        return True
    return False

# Define a new function to generate log entries
def generate_log_entry():
    current_time = time.strftime("%H:%M:%S", time.localtime())
    ip_address = socket.gethostbyname(socket.gethostname())
    request_type, path = urlparse(st.experimental_get_query_params()["__streamlit_app_b64url"][0]).path.split("?", 1)
    return [current_time, ip_address, request_type + path]

# Create the Streamlit app
st.title("Analytical Tool")
server_logs = []

# Create the sidebar
st.sidebar.title("Navigation")
pages = ["Login", "Register", "Dashboard", "Upload CSV"]
page = st.sidebar.selectbox("Select a page", pages)

if page == "Login":
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if login(username, password):
            st.session_state.logged_in = True
            st.success("Login successful!")
            st.write("You are now logged in")
            st.write("You can now access the dashboard")
            server_logs.append(generate_log_entry())
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
        server_logs.append(generate_log_entry())

elif page == "Dashboard" and st.session_state.get("logged_in", False):
    # Create the dashboard
    st.header("Dashboard")
    sport_of_interest = st.selectbox("Select a sport", ["Swimming", "Athletics", "Gymnastics", "Soccer", "Tennis"])
    continent = st.selectbox("Select a continent", ["Asia", "Europe", "Africa", "North America", "South America"])
    country = st.selectbox("Select a country", ["USA", "China", "India", "Russia", "Germany"])

    # Create the visualizations
    data = generate_data(100)
    fig = px.bar(data, x="Country", y="Ranks", color="Sports")
    st.plotly_chart(fig)

    fig = px.pie(data, names="Country", values="Ranks")
    st.plotly_chart(fig)

    # Create the report views
    st.header("Reports")
    report_type = st.selectbox("Select a report type", ["Games played in a day", "Most played sport per country", "Most played sport per gender and country"])
    if report_type == "Games played in a day":
        data = generate_data(100)
        st.write(data.groupby("Match_or_sport_event_dates").count())
    elif report_type == "Most played sport per country":
        data = generate_data(100)
        st.write(data.groupby(["Country", "Sports"]).count())
    elif report_type == "Most played sport per gender and country":
        data = generate_data(100)
        st.write(data.groupby(["Country", "Gender", "Sports"]).count())

elif page == "Upload CSV":
    # Create the CSV upload functionality
    st.header("Upload CSV")
    uploaded_file = st.file_uploader("Select a CSV file", type=["csv"])
    if uploaded_file:
        data = pd.read_csv(uploaded_file)
        st.write(data.head())
        # Perform analysis on the uploaded CSV

# Write server logs to a CSV file
with open('server_logs.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(server_logs)