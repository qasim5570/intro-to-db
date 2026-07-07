import streamlit as st
import pandas as pd
from scripts.data_sync import sync_events_and_weather
from scripts.aggregations import weather_condition_summary, tag_frequency_summary

st.markdown("""
    <div class="weather-banner">
        <h2 style="margin:0;">Admin: Data Refresh</h2>
        <p style="margin:4px 0 0;">Sync events and weather data from external sources</p>
    </div>
""", unsafe_allow_html=True)

with st.container(border=True):
    st.markdown("**Data Sources**")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("🎫 **Eventfinda API**")
        st.caption("Fetches upcoming Sydney events")
    with col2:
        st.markdown("🌤️ **OpenWeather API**")
        st.caption("Fetches current weather per city")

    st.divider()

    if st.button("Run Data Sync Now", use_container_width=True):
        with st.spinner("Syncing events and weather data..."):
            try:
                sync_events_and_weather()
                st.success("Sync completed successfully. Postgres and MongoDB updated.")
            except Exception as e:
                st.error(f"Sync failed: {e}")

st.caption("Note: Re-running sync is safe — existing records are updated via get_or_create and upsert, not duplicated.")

st.divider()
st.subheader("MongoDB Aggregation Insights")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Weather Condition Summary**")
    weather_data = weather_condition_summary()
    if weather_data:
        df_weather = pd.DataFrame([
            {
                "Condition": row["_id"],
                "Event Count": row["event_count"],
                "Avg Temperature (°C)": round(row["average_temperature"], 1),
            }
            for row in weather_data
        ])
        st.dataframe(df_weather, use_container_width=True, hide_index=True)
        st.bar_chart(df_weather.set_index("Condition")["Event Count"])
    else:
        st.info("No weather data available yet. Run a sync first.")

with col2:
    st.markdown("**Tag Frequency Summary**")
    tag_data = tag_frequency_summary()
    if tag_data:
        df_tags = pd.DataFrame([
            {"Tag": row["_id"], "Occurrences": row["count"]}
            for row in tag_data
        ])
        st.dataframe(df_tags, use_container_width=True, hide_index=True)
        st.bar_chart(df_tags.set_index("Tag")["Occurrences"])
    else:
        st.info("No tag data available yet. Run a sync first.")