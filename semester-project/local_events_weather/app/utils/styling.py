import streamlit as st


def apply_custom_style():
    st.markdown("""
        <style>
        [data-testid="stSidebar"] {
            background-color: #0F2B3D;
        }
        [data-testid="stSidebar"] * {
            color: #FFFFFF !important;
        }
        [data-testid="stSidebarNav"] a {
            border-radius: 8px;
            margin: 2px 8px;
            padding: 8px 10px;
        }
        [data-testid="stSidebarNav"] a:hover {
            background-color: #1C6E6E;
        }
        div[data-testid="stVerticalBlockBorderWrapper"] {
            border-radius: 14px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            padding: 4px;
        }
        .stButton > button {
            background-color: #1C6E6E;
            color: white;
            border-radius: 8px;
            border: none;
        }
        .stButton > button:hover {
            background-color: #155757;
        }
        .weather-banner {
            background: linear-gradient(135deg, #0F2B3D, #1C4E5C);
            color: white;
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
        }
        .category-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            margin-bottom: 8px;
        }
        .badge-music { background-color: #E9D8FD; color: #6B21A8; }
        .badge-food { background-color: #FDE9C8; color: #92400E; }
        .badge-sports { background-color: #D1FAE5; color: #065F46; }
        .badge-arts { background-color: #DBEAFE; color: #1E40AF; }
        .badge-family { background-color: #DBEAFE; color: #1E3A8A; }
        .badge-fitness { background-color: #FCE7F3; color: #9D174D; }
        .event-card-image {
            width: 100%;
            height: 180px;
            object-fit: cover;
            border-radius: 10px;
            margin-bottom: 8px;
        }
        .event-detail-image {
            width: 100%;
            height: 320px;
            object-fit: cover;
            border-radius: 12px;
            margin-bottom: 12px;
        }
        </style>
    """, unsafe_allow_html=True)


BADGE_MAP = {
    "Music": "badge-music",
    "Food & Drink": "badge-food",
    "Sports": "badge-sports",
    "Arts & Culture": "badge-arts",
    "Family": "badge-family",
    "Fitness": "badge-fitness",
}


def category_badge_html(category_name):
    css_class = BADGE_MAP.get(category_name, "badge-music")
    return f'<span class="category-badge {css_class}">{category_name}</span>'