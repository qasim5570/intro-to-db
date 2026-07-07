import streamlit as st
from app.db.postgres import SessionLocal
from app.db.mongo import event_details_collection
from app.models import Event, Venue, Category, City
from app.utils.styling import category_badge_html

event_id = st.session_state.get("selected_event_id")
if not event_id:
    st.warning("No event selected. Go back to Browse Events.")
    st.stop()

session = SessionLocal()
event = session.get(Event, event_id)

if not event:
    st.error("Event not found.")
    st.stop()

venue = session.get(Venue, event.venue_id)
category = session.get(Category, event.category_id)
city = session.get(City, venue.city_id) if venue else None

with st.container(border=True):
    detail_doc = event_details_collection.find_one({"event_id": event.event_id})

    if detail_doc and detail_doc.get("image_url"):
        st.image(detail_doc["image_url"], use_container_width=True)

    st.markdown(category_badge_html(category.name), unsafe_allow_html=True)
    st.title(event.title)
    st.write(f"📍 {venue.name}, {city.name}")
    st.write(f"🗓️ {event.start_time} – {event.end_time}")

    if detail_doc:
        st.markdown("### About")
        st.write(detail_doc.get("description", "No description available."))

        if detail_doc.get("tags"):
            st.write("**Tags:** " + ", ".join(detail_doc["tags"]))

        links = detail_doc.get("links", {})
        if links.get("website_url"):
            st.markdown(f"[Event Website]({links['website_url']})")

        weather = detail_doc.get("weather_summary", {})
        if weather:
            st.markdown("### Weather Forecast")
            wcol1, wcol2 = st.columns(2)
            wcol1.metric("Temperature", f"{weather.get('temperature')}°C")
            wcol2.metric("Conditions", weather.get("conditions", "N/A"))
    else:
        st.info("No extended details found in MongoDB for this event.")

    if st.button("♡ Save to My Plans"):
        st.session_state["plan_event_id"] = event.event_id
        st.switch_page("app/pages/3_My_Plans.py")

session.close()