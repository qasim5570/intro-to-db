import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from app.utils.styling import apply_custom_style

st.set_page_config(
    page_title="Local Events Weather Companion",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_custom_style()

pg = st.navigation([
    st.Page(
        "app/pages/1_Browse_Events.py",
        title="Browse Events",
        icon="🗓️",
        default=True,
    ),
    st.Page(
        "app/pages/2_Event_Details.py",
        title="Event Details",
        icon="📄",
    ),
    st.Page(
        "app/pages/3_My_Plans.py",
        title="My Plans",
        icon="❤️",
    ),
    st.Page(
        "app/pages/4_Admin_Data_Refresh.py",
        title="Admin Data Refresh",
        icon="🔄",
    ),
])

pg.run()