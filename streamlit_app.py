import streamlit as st
import pandas as pd
import plotly.express as px
import pycountry
import time
import threading  # Import the threading module
# Function to load and clean data
csv_file= "web_logs.csv"

@st.cache
def load_data():
    # Load data from CSV file
    return pd.read_csv("web_logs.csv")

# Function to periodically check for updates
def check_for_updates():
    while True:
        # Load data
        data = load_and_clean_data("web_logs.csv")
        # Display data in Streamlit app
        st.write(data)
        # Wait for 60 seconds before checking for updates again
        time.sleep(60)
def load_and_clean_data(csv_file):
    # Load raw data from CSV
    raw_data = pd.read_csv(csv_file, header=None)

    # Extract information from raw data
    cleaned_data = raw_data[0].str.extract(r'(\d+\.\d+\.\d+\.\d+) - - \[(.*?)\] - \[(.*?)\]\"(.+?)\" (\d+) (\d+) \"(.+?)\" \"(\w+)\" \"(.+?)\"')

    # Rename the columns
    cleaned_data.columns = ['IP Address', 'Timestamp Start', 'Timestamp End', 'Request', 'Status Code', 'Response Size', 'User Agent', 'Country Code', 'Traffic Source']

    # Convert timestamps to datetime format
    cleaned_data['Timestamp Start'] = pd.to_datetime(cleaned_data['Timestamp Start'], format='%d/%b/%Y:%H:%M:%S')
    cleaned_data['Timestamp End'] = pd.to_datetime(cleaned_data['Timestamp End'], format='%d/%b/%Y:%H:%M:%S')

    return cleaned_data

# Function for dashboard
def dashboard_page(cleaned_data):
    st.title('PAYRIS FUN OLYMPICS DASHBOARD')

    # Create a dropdown menu to select columns
    selected_columns = st.multiselect("Select columns to display", ["Display all columns"] + cleaned_data.columns.tolist())

    # If no columns are selected, display a warning message
    if not selected_columns:
        st.warning("Please select at least one column.")

    # If "Display all columns" option is chosen, display the first 5 records of the entire DataFrame
    elif "Display all columns" in selected_columns:
        st.write(cleaned_data.head())

    # If columns are selected, display the first 5 records with selected columns
    else:
        st.write(cleaned_data[selected_columns].head())

    # Calculate total visits
    total_visits = cleaned_data.shape[0]

    # Calculate number of live sessions from Olympic Channel
    live_sessions_olympic_channel = cleaned_data['Request'].str.contains('/olympic-channel/live-stream').sum()

    # Calculate number of live sessions from Home Page
    live_sessions_home_page = cleaned_data['Request'].str.contains('/home/live-streams').sum()

    # Total live sessions
    total_live_sessions = live_sessions_olympic_channel + live_sessions_home_page

    # Calculate total page views
    total_page_views = cleaned_data['Request'].nunique()

    # Display metrics using st.metric() function
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Visits", total_visits)

    with col2:
        st.metric("Page Views", total_page_views)

    with col3:
        st.metric("Live Sessions", total_live_sessions)
    
    st.subheader("Traffic Analysis")

    # Dropdown menu for selecting analysis options
    analysis_option = st.selectbox("Select analysis option", ["Traffic Per Hour", "Traffic Per Week", "Traffic Per Month"])

    if analysis_option == "Traffic Per Hour":
        # Analyze traffic per hour
        analyze_traffic_per_hour(cleaned_data)
    elif analysis_option == "Traffic Per Week":
        # Analyze traffic per week
        analyze_traffic_per_week(cleaned_data)
    elif analysis_option == "Traffic Per Month":
        # Analyze traffic per month
        analyze_traffic_per_month(cleaned_data)

    # Extract relevant information from User Agent strings
    cleaned_data['Browser'] = cleaned_data['User Agent'].str.extract(r'(?P<Browser>Chrome|Firefox|Edge|Safari)')
    cleaned_data['Device'] = cleaned_data['User Agent'].str.extract(r'(?P<Device>\bAndroid\b|\biPad\b|\biPhone\b|\bWindows\b|\bMacintosh\b|\bLinux\b)')

    # Count occurrences of each unique combination
    browser_counts = cleaned_data['Browser'].value_counts()
    device_counts = cleaned_data['Device'].value_counts()
    traffic_sources = cleaned_data['Traffic Source'].value_counts()
    
    # Assuming cleaned_data contains the relevant column for status codes
    error_data = cleaned_data['Status Code'].value_counts().reset_index()
    error_data.columns = ['Status Code', 'Count']

    # Create two columns for displaying visuals side by side
    col1, col2 = st.columns(2)

    # Add browser distribution visualization to the first column
    with col1:
        st.plotly_chart(px.bar(browser_counts, x=browser_counts.index, y=browser_counts.values, labels={'x': 'Browser', 'y': 'Count'}, title='Browser Distribution', height=350, width= 300))

    # Add device distribution visualization to the second column
    with col2:
        st.plotly_chart(px.bar(device_counts, x=device_counts.index, y=device_counts.values, labels={'x': 'Device', 'y': 'Count'}, title='Device Distribution', height=350, width= 300))
    
    # Add traffic source analysis visualization (Pie chart) to the first column
    with col1:
        st.plotly_chart(px.pie(traffic_sources, values=traffic_sources.values, names=traffic_sources.index, title='Traffic Sources Distribution', height=350, width= 300))

    # Add error analysis visualization (Bar graph) to the second column
    with col2:
        st.plotly_chart(px.bar(error_data, x='Status Code', y='Count', title='Error Analysis', height=350, width= 300 ))

# Function to analyze traffic per hour
def analyze_traffic_per_hour(df):
    # Assuming df contains timestamp_start column
    df['hour'] = pd.to_datetime(df['Timestamp Start']).dt.hour

    # Grouping data by hour and counting the number of requests
    traffic_per_hour = df.groupby('hour').size().reset_index(name='count')

    # Plotting traffic per hour
    fig = px.bar(traffic_per_hour, x='hour', y='count', title='Traffic Per Hour')
    st.plotly_chart(fig)

# Function to analyze traffic per week
def analyze_traffic_per_week(df):
    # Assuming df contains timestamp_start column
    df['week'] = pd.to_datetime(df['Timestamp Start']).dt.isocalendar().week

    # Grouping data by week and counting the number of requests
    traffic_per_week = df.groupby('week').size().reset_index(name='count')

    # Plotting traffic per week
    fig = px.bar(traffic_per_week, x='week', y='count', title='Traffic Per Week')
    st.plotly_chart(fig)

# Function to analyze traffic per month
def analyze_traffic_per_month(df):
    # Assuming df contains timestamp_start column
    df['month'] = pd.to_datetime(df['Timestamp Start']).dt.month

    # Grouping data by month and counting the number of requests
    traffic_per_month = df.groupby('month').size().reset_index(name='count')

    # Plotting traffic per month
    fig = px.bar(traffic_per_month, x='month', y='count', title='Traffic Per Month')
    st.plotly_chart(fig)


# Function for Exploratory Data Analysis
def perform_eda(df):

    # Interactive widgets for exploratory data analysis
    st.title("Exploratory Data Analysis")

    # Display basic statistics
    st.subheader("OLYMPICS BASIC STATISTICS ")
    st.write(df.describe())

    # Country of Origin Analysis
    country_names = {c.alpha_2: c.name for c in pycountry.countries}
    st.subheader("COUNTRY OF ORIGIN ANALYSIS")
    country_visits = df['Country Code'].value_counts()
    
    # Replace country codes with full country names
    country_visits.index = country_visits.index.map(country_names.get)
    
    # Basic Statistics for Country of Origin
    total_visits = df.shape[0]
    st.write(f"Total Number of Visits: {total_visits}")
    
    # Top countries with the highest number of visits
    top_countries = country_visits.head(5)  # Change 5 to the desired number of top countries
    st.write("Top Countries with the Highest Number of Visits:")
    st.write(top_countries)
    
    # Number of Visits Analysis
    st.subheader("NUMBER OF VISITS ANALYSIS")
    
    # Basic summary statistics
    st.subheader("Basic Statistics")
    st.write("Average number of visits per day:")
    st.write(df.groupby(df['Timestamp Start'].dt.date).size().mean())
    st.write("Maximum number of visits in a single day:")
    st.write(df.groupby(df['Timestamp Start'].dt.date).size().max())
    st.write("Minimum number of visits in a single day:")
    st.write(df.groupby(df['Timestamp Start'].dt.date).size().min())
    st.write("Median number of visits per day:")
    st.write(df.groupby(df['Timestamp Start'].dt.date).size().median())
    st.write("Standard deviation of the number of visits per day:")
    st.write(df.groupby(df['Timestamp Start'].dt.date).size().std())
    
    # Number of Visits to Each Page
    st.subheader("Number of Visits to Each Page")
    page_visits = df['Request'].apply(lambda x: x.split()[1]).value_counts()
    st.write("Number of Visits to Each Page:")
    st.write(page_visits)

    # Display popular pages
    st.subheader("Popular Pages")
    popular_pages = page_visits.head(5)  # Display the top 5 most visited pages
    st.write(popular_pages)

    # Percentage distribution of visits across different time periods
    st.subheader("Percentage Distribution of Visits Across Different Time Periods")
    visits_by_day = df['Timestamp Start'].dt.day_name()
    percentage_visits_by_day = visits_by_day.value_counts(normalize=True) * 100
    st.write(percentage_visits_by_day)

    # Traffic source Analysis
    st.subheader("TRAFFIC SOURCE ANALYSIS")
    
    #Pie chart of traffic sources
    traffic_sources = df['Traffic Source'].value_counts()
    fig = px.pie(traffic_sources, values=traffic_sources.values, names=traffic_sources.index,
                 title='Traffic Sources Distribution')
    st.plotly_chart(fig)

    # Basic Statistics for Traffic Sources
    st.subheader("Basic Statistics for Traffic Sources")
    traffic_source_counts = df['Traffic Source'].value_counts()
    st.write("Number of Visits by Traffic Source:")
    st.write(traffic_source_counts)
    st.write("Total Number of Unique Traffic Sources:", len(traffic_source_counts))
    st.write("Most Common Traffic Source:", traffic_source_counts.idxmax())
    
    # Traffic source Analysis
    st.subheader(" ERROR ANALYSIS")
    
    # Distribution of status codes
    st.subheader("Basic Statistics for Status Codes")
    st.write("Distribution of Status Codes:")
    status_code_counts = df['Status Code'].value_counts()
    st.bar_chart(status_code_counts)

    # Basic Statistics for Status Codes
    status_code_counts = df['Status Code'].value_counts()
    st.write("Number of Occurrences by Status Code:")
    st.write(status_code_counts)
    st.write("Total Number of Unique Status Codes:", len(status_code_counts))
    st.write("Most Common Status Code:", status_code_counts.idxmax())

    # MAIN INTERESTS ANALYSIS

    st.subheader("Main Interests (Based on Selected/Viewed Sports)")

    # Top sports
    st.write("Top sports events viewed:")
    top_sports_events = df[df['Request'].str.contains('/sports/')]['Request'].value_counts().head(5)
    st.write(top_sports_events)


    st.subheader("USER ENGAGEMENT")

    st.subheader("Favorites Analysis")
    st.write("Favourites Sports:")
    favorite_sports = df[df['Request'].str.contains('favorite')]['Request'].str.extract(r'/sports/(\w+)/favorite')[0].value_counts()
    st.write(favorite_sports)

    live_streams = df[df['Request'].str.contains('/olympic-channel/live-stream')]
    chats = df[df['Request'].str.contains('/olympic-channel/live-stream/.*/chat')]
    polls = df[df['Request'].str.contains('/olympic-channel/live-stream/.*/poll')]
    share_reactions = df[df['Request'].str.contains('/olympic-channel/live-stream/.*/share-reaction')]

    # Count the number of live stream sessions, chats, polls, and share reactions
    num_live_streams = len(live_streams)
    num_chats = len(chats)
    num_polls = len(polls)
    num_share_reactions = len(share_reactions)

    # Display the results
    st.subheader("Live Stream Analysis")
    st.write("Number of Live Stream Sessions:", num_live_streams)
    st.write("Number of Chats:", num_chats)
    st.write("Number of Polls:", num_polls)
    st.write("Number of Share Reactions:", num_share_reactions)

    # Extract the sports being streamed from the request URLs
    live_streams['Sport'] = live_streams['Request'].str.extract(r'/olympic-channel/live-stream/(\w+)')

    # Calculate the duration of each live stream session
    live_streams['Timestamp Start'] = pd.to_datetime(live_streams['Timestamp Start'])
    live_streams['Timestamp End'] = pd.to_datetime(live_streams['Timestamp End'])
    live_streams['Duration'] = (live_streams['Timestamp End'] - live_streams['Timestamp Start']).dt.total_seconds()

    # Calculate the average duration of live stream sessions for each sport
    average_durations = live_streams.groupby('Sport')['Duration'].mean()

    # Display the average duration of live stream sessions for each sport
    st.subheader("Average Duration of Live Stream Sessions by Sport")
    st.write(average_durations)  


    #Analysing user agents
    st.subheader("USER AGENT ANALYSIS")

    # Extract relevant information from User Agent strings
    df['Browser'] = df['User Agent'].str.extract(r'(?P<Browser>Chrome|Firefox|Edge|Safari)')
    df['Device'] = df['User Agent'].str.extract(r'(?P<Device>\bAndroid\b|\biPad\b|\biPhone\b|\bWindows\b|\bMacintosh\b|\bLinux\b)')

    # Count occurrences of each unique combination
    browser_counts = df['Browser'].value_counts()
    device_counts = df['Device'].value_counts()

    # Create bar charts using Plotly
    fig_browser = px.bar(browser_counts, x=browser_counts.index, y=browser_counts.values, labels={'x': 'Browser', 'y': 'Count'}, title='Browser Distribution')
    fig_device = px.bar(device_counts, x=device_counts.index, y=device_counts.values, labels={'x': 'Device', 'y': 'Count'}, title='Device Distribution')

    # Display the plots
    st.plotly_chart(fig_browser)
    st.plotly_chart(fig_device)

# Function for Upload Own CSV page
def upload_csv_page():
    st.title('Upload Your Own CSV File')
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        st.write("File uploaded successfully!")

        # Read the uploaded CSV file into a DataFrame
        df = pd.read_csv(uploaded_file)

        # Display the DataFrame
        st.write("DataFrame:")
        st.write(df)

        # Display basic statistics
        st.write("Basic Statistics:")
        st.write("Number of Rows:", df.shape[0])
        st.write("Number of Columns:", df.shape[1])
        st.write("Column Data Types:")
        st.write(df.dtypes)

        # Summary statistics for numeric columns
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            st.write("Summary Statistics for Numeric Columns:")
            st.write(df[numeric_cols].describe())


# Main function
def main():
    # st.sidebar.image("logo\eizatheedev.png", caption="PAYRIS FUN OLYMPICS" )
    selected_page = st.sidebar.radio("Go to", ["Upload Own CSV", "Dashboard", "Exploratory Data Analysis"])

    if selected_page == "Upload Own CSV":
        upload_csv_page()
    elif selected_page == "Dashboard":
        cleaned_data = load_and_clean_data("web_logs.csv")
        dashboard_page(cleaned_data)
    elif selected_page == "Exploratory Data Analysis":
        df = load_and_clean_data("web_logs.csv")
        perform_eda(df)

    # Start a background thread to check for updates
    thread = threading.Thread(target=check_for_updates)
    # Wait for the thread to start
    thread.start()  

if __name__ == "__main__":
    main()
