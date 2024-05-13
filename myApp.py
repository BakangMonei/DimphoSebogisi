import streamlit as st
import pandas as pd
import random
import plotly.express as px

# Define the data attributes
ATTRIBUTES = [
    "Username",
    "Password"
]

# Define the login and registration functions
def login(username, password):
    # Read usernames and passwords from CSV file
    df = pd.read_csv("user_credentials.csv")
    if (df['Username'] == username).any() and (df[df['Username'] == username]['Password'].iloc[0] == password):
        return True
    return False

def register(username, password):
    # Append new registration to the CSV file
    new_data = pd.DataFrame({'Username': [username], 'Password': [password]})
    with open("user_credentials.csv", "a") as file:
        new_data.to_csv(file, header=False, index=False)
    return True

# Create the Streamlit app
st.title("Analytical Tool")

# Create the sidebar
st.sidebar.title("Navigation")
pages = ["Login", "Register", "Dashboard", "Upload CSV"]
page = st.sidebar.selectbox("Select a page", pages)

if page == "Login":
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if login(username, password):
            st.success("Login successful!")
            page = "Dashboard"  # Automatically switch to dashboard after successful login
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

if page == "Dashboard":
    # Create the dashboard
    st.header("Dashboard")
    sport_of_interest = st.selectbox("Select a sport", ["Swimming", "Athletics", "Gymnastics", "Soccer", "Tennis"])
    continent = st.selectbox("Select a continent", ["Asia", "Europe", "Africa", "North America", "South America"])
    country = st.selectbox("Select a country", ["USA", "China", "India", "Russia", "Germany"])

    # Create the visualizations
    @st.cache
    def generate_data(n_rows):
        data = []
        for _ in range(n_rows):
            row = {
                "Country": random.choice(["USA", "China", "India", "Russia", "Germany"]),
                "Sports": random.choice(["Swimming", "Athletics", "Gymnastics", "Soccer", "Tennis"]),
                "Ranks": random.randint(1, 10)
            }
            data.append(row)
        return pd.DataFrame(data)

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
        st.write(data.groupby("Country").size())
    elif report_type == "Most played sport per country":
        data = generate_data(100)
        st.write(data.groupby(["Country", "Sports"]).size())
    elif report_type == "Most played sport per gender and country":
        data = generate_data(100)
        st.write(data.groupby(["Country", "Sports"]).size())

elif page == "Upload CSV":
    # Create the CSV upload functionality
    st.header("Upload CSV")
    uploaded_file = st.file_uploader("Select a CSV file", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write(df.head())
