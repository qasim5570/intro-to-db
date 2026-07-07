import os
import time
import requests
from dotenv import load_dotenv


load_dotenv()


EVENTFINDA_USER = os.getenv("EVENTFINDA_USER")
EVENTFINDA_API_KEY = os.getenv("EVENTFINDA_API_KEY")


LOCATIONS_URL = "https://api.eventfinda.com.au/v2/locations.json"
EVENTS_URL = "https://api.eventfinda.com.au/v2/events.json"



def get_location_id(name="Sydney"):
    """
    Looks up the numeric location ID for a given place name.
    Returns the first matching location's ID immediately.
    """
    params = {"q": name, "rows": 5}
    response = requests.get(
        LOCATIONS_URL,
        params=params,
        auth=(EVENTFINDA_USER, EVENTFINDA_API_KEY),
        timeout=15
    )
    if response.status_code != 200:
        raise Exception(f"Eventfinda locations error {response.status_code}: {response.text}")


    data = response.json()
    locations = data.get("locations", [])
    if not locations:
        raise Exception(f"No location found for '{name}'")


    first = locations[0]
    print(f"Using location: {first.get('name')} (id={first.get('id')})")
    return first["id"]



def fetch_sydney_events(rows=20, max_retries=3):
    """
    Fetches events located in Sydney from the Eventfinda API,
    with retry handling for transient timeouts.
    """
    location_id = get_location_id("Sydney")


    params = {
        "location": location_id,
        "rows": rows,
        "fields": "categories,point,description,images,location,location_summary"
    }


    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(
                EVENTS_URL,
                params=params,
                auth=(EVENTFINDA_USER, EVENTFINDA_API_KEY),
                timeout=30
            )
            if response.status_code != 200:
                raise Exception(f"Eventfinda API error {response.status_code}: {response.text}")
            data = response.json()
            return data.get("events", [])
        except requests.exceptions.Timeout:
            print(f"⚠️ Attempt {attempt} timed out. Retrying...")
            time.sleep(2)
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Attempt {attempt} failed: {e}")
            time.sleep(2)


    raise Exception("Failed to fetch events after multiple retries.")



if __name__ == "__main__":
    events = fetch_sydney_events(rows=5)
    print(f"Fetched {len(events)} events.")
    for e in events[:2]:
        print(e.get("name"), "-", e.get("datetime_start"))
        print(e.get("location"))