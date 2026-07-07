from datetime import datetime, timezone
from app.services.eventfinda_client import fetch_sydney_events
from app.services.openweather_client import fetch_weather
from app.db.postgres import SessionLocal
from app.db.mongo import db as mongo_db
from app.models import City, Venue, Category, Event



def get_or_create(session, model, defaults=None, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    params = {**kwargs, **(defaults or {})}
    instance = model(**params)
    session.add(instance)
    session.flush()
    return instance



def sync_events_and_weather():
    session = SessionLocal()
    events_raw = fetch_sydney_events(rows=20)


    for ev in events_raw:
        city = get_or_create(session, City, name="Sydney", country="AU")

        location_data = ev.get("location", {})
        venue = get_or_create(
            session, Venue,
            name=location_data.get("name", "Unknown Venue"),
            defaults={
                "address": location_data.get("address") or ev.get("location_summary", ""),
                "city_id": city.city_id,
            },
            city_id=city.city_id,
        )
        category = get_or_create(
            session, Category,
            name=ev.get("category", {}).get("name", "General"),
        )


        event = get_or_create(
            session, Event,
            source_event_id=str(ev.get("id")),
            defaults={
                "title": ev.get("name"),
                "start_time": ev.get("datetime_start"),
                "end_time": ev.get("datetime_end"),
                "venue_id": venue.venue_id,
                "category_id": category.category_id,
            },
        )


        weather_raw = fetch_weather(city="Sydney")


        weather_response_doc = {
            "city_id": city.city_id,
            "requested_at": datetime.now(timezone.utc).isoformat(),
            "response": weather_raw,
        }


        mongo_db.weather_api_responses.update_one(
            {"city_id": city.city_id},
            {"$set": weather_response_doc},
            upsert=True,
        )


        images_data = ev.get("images", {}).get("images", [])
        primary_image = next((img for img in images_data if img.get("is_primary")), None)
        image_url = primary_image.get("original_url") if primary_image else (
            images_data[0].get("original_url") if images_data else None
        )


        event_detail_doc = {
            "event_id": event.event_id,
            "description": ev.get("description", ""),
            "tags": ev.get("tags", []),
            "image_url": image_url,
            "links": {
                "website_url": ev.get("url", ""),
                "ticket_url": ev.get("ticket_url", ""),
            },
            "weather_summary": {
                "temperature": weather_raw.get("main", {}).get("temp"),
                "conditions": weather_raw.get("weather", [{}])[0].get("main", ""),
                "retrieved_at": datetime.now(timezone.utc).isoformat(),
            },
        }


        mongo_db.event_details.update_one(
            {"event_id": event.event_id},
            {"$set": event_detail_doc},
            upsert=True,
        )


    session.commit()
    session.close()
    print(f"Synced {len(events_raw)} events with weather data.")



if __name__ == "__main__":
    sync_events_and_weather()