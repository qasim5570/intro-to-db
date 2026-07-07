from datetime import datetime
from app.db.mongo import (
    event_details_collection,
    weather_api_responses_collection,
    user_notes_collection,
)

event_details_collection.delete_many({})
weather_api_responses_collection.delete_many({})
user_notes_collection.delete_many({})

event_details_collection.insert_one({
    "event_id": 101,
    "description": "Outdoor night market with live music and food stalls.",
    "tags": ["family-friendly", "free-entry", "outdoor"],
    "links": {
        "website_url": "https://example.com/event/101",
        "ticket_url": "https://example.com/tickets/101"
    },
    "weather_summary": {
        "temperature": 18,
        "conditions": "Cloudy",
        "retrieved_at": datetime(2026, 6, 20, 10, 0, 0)
    }
})

weather_api_responses_collection.insert_one({
    "city_id": 5,
    "requested_at": datetime(2026, 6, 20, 9, 0, 0),
    "response": {
        "coord": {"lon": 151.21, "lat": -33.87},
        "weather": [{"main": "Clouds", "description": "broken clouds"}],
        "main": {"temp": 18.4, "humidity": 67},
        "wind": {"speed": 4.1}
    }
})

user_notes_collection.insert_one({
    "user_id": 2,
    "event_id": 101,
    "notes": [
        {
            "note_id": 1,
            "created_at": datetime(2026, 6, 18, 14, 30, 0),
            "text": "Check transport options before leaving."
        },
        {
            "note_id": 2,
            "created_at": datetime(2026, 6, 19, 12, 15, 0),
            "text": "Invite two friends from class."
        }
    ]
})

print("✅ Sample documents inserted into all 3 MongoDB collections.")