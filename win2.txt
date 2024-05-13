import streamlit as st
import pandas as pd
import logging
import random
import time
import plotly.graph_objs as go

class LogGenerator:
    def __init__(self):
        self.logs = []

    def generate_log(self):
        log_message = {
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
        self.logs.append(log_message)

    def save_logs_to_csv(self, filename):
        logs_df = pd.DataFrame(self.logs)
        logs_df.to_csv(filename, index=False)

class LogVisualizer:
    def __init__(self):
        self.log_generator = LogGenerator()

    def generate_and_save_logs(self, num_logs, filename):
        for i in range(num_logs):
            self.log_generator.generate_log()
        self.log_generator.save_logs_to_csv(filename)

    def visualize_logs(self, filename):
        logs_df = pd.read_csv(filename)
        st.write("Logs:")
        st.dataframe(logs_df)

        # Pie chart for country of origin
        country_counts = logs_df['Country'].value_counts()
        fig1 = go.Figure(data=[go.Pie(labels=country_counts.index, values=country_counts.values)])
        st.plotly_chart(fig1)

        # Line chart for number of visits over time
        visits_df = logs_df.groupby('Timestamp').size().reset_index(name='counts')
        fig2 = go.Figure(data=[go.Scatter(x=visits_df['Timestamp'], y=visits_df['counts'], mode='lines')])
        st.plotly_chart(fig2)

        # Bar chart for main interests
        interest_counts = logs_df['Sports'].value_counts()
        fig3 = go.Figure(data=[go.Bar(x=interest_counts.index, y=interest_counts.values)])
        st.plotly_chart(fig3)

class ServerLogs:
    def __init__(self):
        self.server_logs = []

    def generate_server_log(self, ip_address, request_type, status_code, log_data):
        log_message = {
            "Timestamp": pd.Timestamp.now(),
            "IP_Address": ip_address,
            "Request_Type": request_type,
            "Status_Code": status_code,
            "Log_Data": log_data
        }
        self.server_logs.append(log_message)

    def save_server_logs_to_csv(self, filename):
        server_logs_df = pd.DataFrame(self.server_logs)
        server_logs_df.to_csv(filename, index=False)

    def visualize_server_logs(self, filename):
        server_logs_df = pd.read_csv(filename)
        st.write("Server Logs:")
        st.dataframe(server_logs_df)

def main():
    logging.basicConfig(level=logging.INFO)

    st.title("Streamlit Log Analyzer")

    num_logs = st.sidebar.slider("Number of Logs", 10, 1000, 500)

    if st.sidebar.button("Generate Logs"):
        log_visualizer = LogVisualizer()
        log_visualizer.generate_and_save_logs(num_logs, "logs.csv")
        log_visualizer.visualize_logs("logs.csv")

        server_logs = ServerLogs()
        for i in range(num_logs):
            log_data = log_visualizer.log_generator.logs[i]
            server_logs.generate_server_log("127.0.0.1", "GET", 200, log_data)
        server_logs.save_server_logs_to_csv("server_logs.csv")
        server_logs.visualize_server_logs("server_logs.csv")

    if st.sidebar.button("Analyze Data"):
        st.write("Navigate to the Analyzer tab to analyze data.")

    if st.sidebar.button("Visualize Logs"):
        st.write("Navigate to the Visualizer tab to visualize logs.")

    if st.sidebar.button("Server Logs"):
        st.write("Navigate to the Server Logs tab to view server logs.")

if __name__ == "__main__":
    main()