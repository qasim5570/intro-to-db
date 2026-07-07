import streamlit as st
from sqlalchemy import select
from app.db.postgres import SessionLocal
from app.db.mongo import weather_api_responses_collection, event_details_collection
from app.models import Event, Venue, Category, City
from app.utils.styling import category_badge_html

session = SessionLocal()

city_row = session.query(City).first()
weather_doc = weather_api_responses_collection.find_one({"city_id": city_row.city_id}) if city_row else None
weather = weather_doc.get("response", {}) if weather_doc else {}
temp = weather.get("main", {}).get("temp", "--")
condition = weather.get("weather", [{}])[0].get("description", "N/A").title()

st.markdown(f"""
    <div class="weather-banner">
        <h2 style="margin:0;">{city_row.name if city_row else 'City'}</h2>
        <p style="margin:4px 0 12px;">Live weather snapshot</p>
        <h1 style="margin:0;">{temp}°C</h1>
        <p style="margin:4px 0;">{condition}</p>
    </div>
""", unsafe_allow_html=True)

st.subheader("Upcoming Events")

query = (
    select(Event, Venue, Category, City)
    .join(Venue, Event.venue_id == Venue.venue_id)
    .join(Category, Event.category_id == Category.category_id)
    .join(City, Venue.city_id == City.city_id)
    .order_by(Event.start_time)
)
results = session.execute(query).all()

if not results:
    st.info("No events found. Run Admin Data Refresh first.")
else:
    cols = st.columns(3)
    for idx, (event, venue, category, city) in enumerate(results):
        with cols[idx % 3]:
            with st.container(border=True):
                detail_doc = event_details_collection.find_one({"event_id": event.event_id})
                image_url = detail_doc.get("image_url") if detail_doc else None

                if image_url:
                    st.image(image_url, use_container_width=True)
                else:
                    st.image("https://via.placeholder.com/300x180?text=No+Image", use_container_width=True)

                st.markdown(category_badge_html(category.name), unsafe_allow_html=True)
                st.markdown(f"**{event.title}**")
                st.caption(f"📍 {venue.name}, {city.name}")
                st.caption(f"🗓️ {event.start_time}")
                if st.button("View Details", key=f"view_{event.event_id}"):
                    st.session_state["selected_event_id"] = event.event_id
                    st.switch_page("app/pages/2_Event_Details.py")

session.close()