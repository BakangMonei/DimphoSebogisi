import requests
import csv
from datetime import datetime
import time

# Function to fetch data from the API
def fetch_raw_data_from_api():
    api_url = "http://127.0.0.1:5000/generate-logs"  # Replace this with the actual URL of your API
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error: Failed to retrieve data from the API")
        return None


# Function to save data to a CSV file
def save_raw_to_csv(raw_data):
    if raw_data:
        print("Raw data received:", raw_data)
        print("Number of raw log entries:", len(raw_data))
        csv_filename = "web_logs.csv"
        with open(csv_filename, "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            # Write each raw log entry to the CSV file
            for raw_log in raw_data:
                writer.writerow([raw_log])
        print(f"Raw data saved to CSV file: {csv_filename}")
    else:
        print("No raw data to save.")


# Main function
def main():
    # Infinite loop to continuously fetch data
    while True:
        # Fetch raw data from the API
        raw_data = fetch_raw_data_from_api()
        print("Raw data fetched from API:", raw_data)  # Print the fetched raw data
        
        # Save raw data to CSV file
        save_raw_to_csv(raw_data)

        # Sleep for 1 minute before fetching data again
        time.sleep(60)  # Sleep for 60 seconds (1 minute)

if __name__ == "__main__":
    main()
