import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Compare Sentiment", layout="wide")

# Page design and background styling
st.markdown("""
    <style>
    .stApp { background-color: #e6ebe0; }

    header[data-testid="stHeader"] {
        background-color: #e6ebe0;
    }

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
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <h1 style='text-align: center; color: #2C3E50;'>Compare Sentiment Distribution</h1>
""", unsafe_allow_html=True)

review = pd.read_csv("/Users/macbookpro/code/HayaAlsubie/Beyond_the_Stars/data/cleaned_reviews.csv")

# REGION AND CITY FILTERS
regions = review["Region"].dropna().unique()
cities = review["City"].dropna().unique()
place_types = ["All"] + sorted(review["Place Type"].dropna().unique())

col1, col2 = st.columns(2)

with col1:
    selected_region_1 = st.selectbox("Select First Region", regions, index=0)
    selected_city_1 = st.selectbox("Select City in First Region (Optional)", ["All Cities"] + list(review[review["Region"] == selected_region_1]["City"].dropna().unique()))

with col2:
    selected_region_2 = st.selectbox("Select Second Region", regions, index=1)
    selected_city_2 = st.selectbox("Select City in Second Region (Optional)", ["All Cities"] + list(review[review["Region"] == selected_region_2]["City"].dropna().unique()))

selected_place_type = st.selectbox("Select Place Type", place_types)

# FILTERING DATA

# Filter for Region 1
if selected_city_1 != "All Cities":
    data_region_1 = review[(review["Region"] == selected_region_1) & (review["City"] == selected_city_1)]
else:
    data_region_1 = review[review["Region"] == selected_region_1]

# Filter for Region 2
if selected_city_2 != "All Cities":
    data_region_2 = review[(review["Region"] == selected_region_2) & (review["City"] == selected_city_2)]
else:
    data_region_2 = review[review["Region"] == selected_region_2]

# Filter by place type if selected
if selected_place_type != "All":
    data_region_1 = data_region_1[data_region_1["Place Type"] == selected_place_type]
    data_region_2 = data_region_2[data_region_2["Place Type"] == selected_place_type]

# CHARTS

if selected_region_1 == selected_region_2 and selected_city_1 == selected_city_2:
    st.warning("⚠️ Please select two different regions or cities to compare.")
else:
    col3, col4 = st.columns(2)

    with col3:
        st.markdown(f"<h3 style='text-align: center; color: #CBA135;'>Sentiment in: {selected_region_1}</h3>", unsafe_allow_html=True)
        fig1 = px.histogram(data_region_1, x="Predicted Sentiment Label", color="Predicted Sentiment Label",
                            color_discrete_sequence=["#6ba292", "#d77c7c"],
                            template="simple_white")
        fig1.update_layout(showlegend=False, paper_bgcolor="rgba(0,0,0,0)",
                           plot_bgcolor="rgba(0,0,0,0)", yaxis=dict(range=[0, 3000]))
        st.plotly_chart(fig1, use_container_width=True)

    with col4:
        st.markdown(f"<h3 style='text-align: center; color: #CBA135;'>Sentiment in: {selected_region_2}</h3>", unsafe_allow_html=True)
        fig2 = px.histogram(data_region_2, x="Predicted Sentiment Label", color="Predicted Sentiment Label",
                            color_discrete_sequence=["#6ba292", "#d77c7c"],
                            template="simple_white")
        fig2.update_layout(showlegend=False, paper_bgcolor="rgba(0,0,0,0)",
                           plot_bgcolor="rgba(0,0,0,0)", yaxis=dict(range=[0, 3000]))
        st.plotly_chart(fig2, use_container_width=True)
