import streamlit as st
import pandas as pd
import plotly.express as px

# ───────────────────────────────────────────────
# PAGE CONFIGURATION
# ───────────────────────────────────────────────
st.set_page_config(page_title="Compare Sentiment", layout="wide")

# ───────────────────────────────────────────────
# LOAD DATA
# ───────────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_csv("notebooks/review_data.csv")

review = load_data()

# ───────────────────────────────────────────────
# PAGE STYLING
# ───────────────────────────────────────────────
st.markdown("""
    <style>
    /* Page background */
    .stApp { background-color: #e6ebe0; }

    /* Remove white header bar */
    header[data-testid="stHeader"] {
        background-color: #e6ebe0;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #153f2e;
    }
    section[data-testid="stSidebar"] * {
        color: #e6ebe0;
    }
    [data-testid="stSidebarNav"] ul li a {
        color: #e6ebe0;
        font-weight: 500;
    }
    [data-testid="stSidebarNav"] ul li a[aria-current="page"] {
        color: #CBA135;
        font-weight: bold;
    }

    /* Select Box Styling */
    .filter-container label {
        color: #BFA76F;
        font-weight: 600;
        display: block;
        margin-bottom: 0.5rem;
    }
    .filter-container .stSelectbox, .filter-container .stMultiSelect {
        width: 100%;
    }

    .selectbox-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    </style>
""", unsafe_allow_html=True)

# ───────────────────────────────────────────────
# PAGE TITLE
# ───────────────────────────────────────────────
st.markdown("<h1 style='text-align: center;'>Compare Sentiment Distribution</h1>", unsafe_allow_html=True)

# ───────────────────────────────────────────────
# FILTERS
# ───────────────────────────────────────────────
regions = review["Region"].unique().tolist()

col1, col2 = st.columns(2)

with col1:
    selected_region_1 = st.selectbox("Select First Region", options=regions, index=0)
    cities_1 = review[review["Region"] == selected_region_1]["City"].unique().tolist()
    selected_city_1 = st.selectbox("Select City in First Region (Optional)", options=["All Cities"] + cities_1)

with col2:
    selected_region_2 = st.selectbox("Select Second Region", options=regions, index=1 if len(regions) > 1 else 0)
    cities_2 = review[review["Region"] == selected_region_2]["City"].unique().tolist()
    selected_city_2 = st.selectbox("Select City in Second Region (Optional)", options=["All Cities"] + cities_2)

# Align Place Type selection to center
st.markdown("""
<div class="selectbox-container">
    <label>Select Place Type</label>
""", unsafe_allow_html=True)

place_types_all = review["Place Type"].unique().tolist()
selected_place_type = st.selectbox("Select Place Type", options=["All"] + place_types_all, label_visibility="collapsed")

st.markdown("</div>", unsafe_allow_html=True)

# ───────────────────────────────────────────────
# FILTER DATA
# ───────────────────────────────────────────────
def filter_data(region, city):
    df = review[review["Region"] == region]
    if city != "All Cities":
        df = df[df["City"] == city]
    if selected_place_type != "All":
        df = df[df["Place Type"] == selected_place_type]
    return df

data_region_1 = filter_data(selected_region_1, selected_city_1)
data_region_2 = filter_data(selected_region_2, selected_city_2)

# ───────────────────────────────────────────────
# CHARTS
# ───────────────────────────────────────────────
col3, col4 = st.columns(2)

with col3:
    st.markdown(f"<h3 style='text-align: center; color: #CBA135;'>Sentiment in: {selected_region_1}</h3>", unsafe_allow_html=True)
    fig1 = px.histogram(data_region_1, x="Sentiment Label", color="Sentiment Label",
                        color_discrete_sequence=["#6ba292", "#5c305c", "#d77c7c"],
                        template="simple_white")
    fig1.update_layout(showlegend=False, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig1, use_container_width=True)

with col4:
    st.markdown(f"<h3 style='text-align: center; color: #CBA135;'>Sentiment in: {selected_region_2}</h3>", unsafe_allow_html=True)
    fig2 = px.histogram(data_region_2, x="Sentiment Label", color="Sentiment Label",
                        color_discrete_sequence=["#6ba292", "#5c305c", "#d77c7c"],
                        template="simple_white")
    fig2.update_layout(showlegend=False, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig2, use_container_width=True)
