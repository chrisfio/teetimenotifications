import requests
import time
import random
from datetime import datetime
from twilio.rest import Client

# your Twilio account SID and auth token, which you can get from the Twilio console
account_sid = '<your_account_sid>'
auth_token = '<your_auth_token>'

client = Client(account_sid, auth_token)
count = 0

url = "https://www.chronogolf.com/marketplace/clubs/18159/teetimes?date=2024-04-27&course_id=21182&affiliation_type_ids%5B%5D=85113&affiliation_type_ids%5B%5D=85113&nb_holes=18"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.69.0 Safari/537.36",
}

try:
    while True:
        try:
            # replace with your API URL
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            data = response.json()  # converts the response to a Python dictionary
            # Iterate over each tee time object
            for obj in data:
                start_time = datetime.strptime(obj['start_time'], "%H:%M")
                lower_limit = datetime.strptime("11:10", "%H:%M")
                upper_limit = datetime.strptime("12:30", "%H:%M")

                # checks if "out_of_capacity" is False
                if lower_limit <= start_time <= upper_limit and obj['out_of_capacity'] is False:
                    message = client.messages.create(
                        # hold - fix twilio limiting body="A tee time at {} has opened up!".format(obj['start_time']),
                        body="A tee time at has opened up at Laytonsville!",
                        from_='+18667573768',  # a Twilio number you've bought
                        to='+14439042141'  # the phone number you want to send a message to
                    )
                    print("Message sent, exiting...")
                    exit(0)  # stop the script
            count += 1
            print("Test {} - Response {}".format(count, response.status_code))

        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
        except requests.exceptions.ConnectionError as e:
            print(f"Connection Error: {e}")
        except requests.exceptions.Timeout as e:
            print(f"Timeout Error: {e}")
        except requests.exceptions.RequestException as e:
            print(f"Request Exception: {e}")

        # wait for between 6 and 11 minutes before the next API call
        time.sleep(random.randint(360, 660))
except KeyboardInterrupt:
    print("Script terminated by user.")
