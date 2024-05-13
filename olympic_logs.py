from flask import Flask, jsonify
import random
from datetime import datetime, timedelta
import pycountry

app = Flask(__name__)

# List of example pages on the Olympic online broadcasting platform
pages = ['/home', '/sports', '/olympic-channel', '/news', '/schedule']

# List of example sports events
sports_events = ['Athletics', 'Basketball', 'Badminton', 'Cricket', 'Diving', 'Fencing', 'Football', 'Golf', 'hockey', 'Gymnastics', 'karate', 'Swimming', 'Tennis', 'Volleyball', 'Weightlifting']

# List of example HTTP methods
http_methods = ['GET', 'POST']

# List of example status codes
status_codes = [200, 301, 404, 500]

# List of traffic sources
traffic_sources = ['Organic Search', 'Direct Search', 'Paid Advertising', 'Facebook', 'Youtube', 'Twitter']

# List of example user agents from different browsers and devices
user_agents = [
    # Windows Browsers
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/17.17134 Safari/537.36",
    # macOS Browsers
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/61.0",
    # Linux Browsers
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0",
    # Mobile Browsers
    "Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 11_2_6 like Mac OS X) AppleWebKit/604.5.6 (KHTML, like Gecko) Version/11.0 Mobile/15D100 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 9; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Mobile Safari/537.36",
    # Tablet Browsers
    "Mozilla/5.0 (iPad; CPU OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Mobile/15E148 Safari/604.1",  # iPad
    "Mozilla/5.0 (Linux; Android 8.0.0; SM-T350 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.101 Safari/537.36",  # Android Tablet
    "Mozilla/5.0 (Linux; Android 9; SM-T350) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.101 Safari/537.36"  # Android Tablet
]

# Function to generate a single log entry within a specific date range
def generate_raw_log_entry(start_date, end_date):
    ip_address = '.'.join(str(random.randint(0, 255)) for _ in range(4))
    timestamp_start = (start_date + timedelta(seconds=random.randint(0, int((end_date - start_date).total_seconds())))).strftime("%d/%b/%Y:%H:%M:%S")
    session_duration = random.randint(60, 3600)  # Random session duration between 1 minute and 1 hour (in seconds)
    timestamp_end = (datetime.strptime(timestamp_start, "%d/%b/%Y:%H:%M:%S") + timedelta(seconds=session_duration)).strftime("%d/%b/%Y:%H:%M:%S")
    http_method = random.choice(http_methods)
    page = random.choice(pages)
    request = f'{http_method} {page} HTTP/1.1'

    if page == '/home':
        if random.random() < 0.4:  # 20% chance of accessing upcoming events
            request = 'GET /home/upcoming-events HTTP/1.1'
        elif random.random() < 0.6:  # 20% chance of accessing popular videos
            request = 'GET /home/popular-videos HTTP/1.1'
        elif random.random() < 0.8:  # 20% chance of accessing news updates
            request = 'GET /home/news-updates HTTP/1.1'
        else: 
            request = 'GET /home/highlights HTTP/1.1'
    elif page == '/news':
        category = random.choice(['sports', 'entertainment', 'politics', 'technology'])
        request = f'GET /news/{category} HTTP/1.1'    
    elif page == '/olympic-channel':
        sports_event = random.choice(sports_events)
        if random.random() < 0.5:  # 20% chance of joining/ watching live stream sessions  
            request = f'POST /olympic-channel/live-stream/{sports_event} HTTP/1.1'
        elif random.random() < 0.8:  # 30% chance of interacting with live chat, polls, or reactions that are related to the sport being live streamed
            request = random.choice([f'POST /olympic-channel/live-stream/{sports_event}/chat HTTP/1.1', f'POST /olympic-channel/live-stream/{sports_event}/poll HTTP/1.1', f'POST /olympic-channel/live-stream/{sports_event}/share-reaction HTTP/1.1'])
        else:  # 50% chance of ending live stream
            request = f'POST /olympic-channel/live-stream/{sports_event}/end HTTP/1.1'  # Example: Ending live stream for a specific sport
    elif page == '/sports':
        if random.random() < 0.3:   # 30% chance of browsing sports categories
            sport_event = random.choice(['Athletics', 'Basketball', 'Badminton', 'Cricket', 'Diving', 'Fencing', 'Football', 'Golf', 'hockey','Gymnastics', 'karate', 'Swimming', 'Tennis', 'Volleyball', 'Weightligting'])
            request = f'GET /sports/{sport_event} HTTP/1.1'
        elif random.random() < 0.6:  # 30% chance of checking the schedule
            request = 'GET /sports/schedule HTTP/1.1'
        else:  # 40% chance of favoriting or following specific sports
            sport = random.choice(['Athletics', 'Basketball', 'Badminton', 'Cricket', 'Diving', 'Fencing', 'Football', 'Golf', 'hockey','Gymnastics', 'karate', 'Swimming', 'Tennis', 'Volleyball', 'Weightligting'])
            request = f'POST /sports/{sport}/favorite HTTP/1.1'

    status_code = random.choice(status_codes)
    response_size = random.randint(100, 1000)
    user_agent = random.choice(user_agents)
    country_code = random.choice(list(pycountry.countries)).alpha_2
    traffic_source = random.choice(traffic_sources)  # Randomly select a traffic source
    return f"{ip_address} - - [{timestamp_start}] - [{timestamp_end}]\"{request}\" {status_code} {response_size} \"{user_agent}\" \"{country_code}\" \"{traffic_source}\""

# Function to generate logs within a specific date range
def generate_raw_logs(start_date, end_date, num_logs):
    raw_logs = []
    for _ in range(num_logs):
        raw_log_entry = generate_raw_log_entry(start_date, end_date)
        raw_logs.append(raw_log_entry)
    return raw_logs

@app.route('/')
def index():
    return "Welcome to the Payris fun Olympic Log Generator API. To generate logs, please visit the '/generate-logs' endpoint."

@app.route('/generate-logs', methods=['GET'])
def get_raw_logs():
    start_date = datetime(2024, 6, 30)
    end_date = datetime(2024, 8, 30)
    num_logs = 1500
    raw_logs = generate_raw_logs(start_date, end_date, num_logs)
    return jsonify(raw_logs)

if __name__ == '__main__':
    app.run(debug=True)