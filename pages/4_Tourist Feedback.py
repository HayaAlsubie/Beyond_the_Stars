import streamlit as st
import pandas as pd
import plotly.express as px

# ────────────────────────────────
# PAGE CONFIG & STYLING
# ────────────────────────────────
st.markdown("""
<style>
.stApp {
    background-color: #e6ebe0;
    color: black;
}
header[data-testid="stHeader"] {
    background-color: #e6ebe0 !important;
}
section[data-testid="stSidebar"] {
    background-color: #153f2e !important;
}
section[data-testid="stSidebar"] * {
    color: #e6ebe0 !important;
}
[data-testid="stSidebarNav"] ul li a {
    color: #e6ebe0 !important;
    font-weight: 500;
}
[data-testid="stSidebarNav"] ul li a[aria-current="page"] {
    color: #CBA135 !important;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ────────────────────────────────
# COLOR SETUP
# ────────────────────────────────
region_colors = {
    "Central": "#6C91BF",
    "West": "#E08626",
    "East": "#5DA15D",
    "North": "#D65C5C",
    "South": "#A87EB4"
}

sentiment_colors = {
    "positive": "#6DBE94",
    "neutral": "#A9A9A9",
    "negative": "#D26464"
}

# ────────────────────────────────
# LOAD DATA
# ────────────────────────────────
@st.cache_data
def load_data():

    return pd.read_csv("data/cleaned_reviews.csv")


review = load_data()



# ────────────────────────────────
# SECTION 1: PAGE TITLE
# ────────────────────────────────
st.markdown("<h1 style='text-align: center;'>Tourist Feedback Analysis Across Saudi Regions</h1>", unsafe_allow_html=True)



st.markdown("<br>", unsafe_allow_html=True)


# ────────────────────────────────
# SECTION 2: SENTIMENT DISTRIBUTION
# ────────────────────────────────
type_sentiment = review.groupby(["Place Type", "Predicted Sentiment Label"]).size().reset_index(name="Count")

st.markdown("<h2>Sentiment Trends by Type of Place</h2>", unsafe_allow_html=True)
st.markdown("""
<p style='text-align: center;'>
This chart shows how tourists feel about different types of places.
It helps identify where people are generally satisfied or dissatisfied.
</p>
""", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

fig2 = px.bar(
    type_sentiment,
    x="Place Type",
    y="Count",
    color="Predicted Sentiment Label",
    barmode="stack",
    color_discrete_map=sentiment_colors
)
fig2.update_layout(xaxis_tickangle=-45, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig2, use_container_width=True)

# ────────────────────────────────
# SECTION 3: CITIES NEEDING ATTENTION
# ────────────────────────────────
st.markdown("<h2>Regions with Most Concerning Cities</h2>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<p style='text-align: center;'>
This chart shows which regions have the highest number of cities with low ratings and negative feedback.
It helps prioritize improvement efforts on a regional scale.
</p>
""", unsafe_allow_html=True)

total_reviews = review.groupby(['Region', 'City']).size().reset_index(name='Total Reviews')
neg_reviews = review[review['Predicted Sentiment Label'] == 'negative'].groupby(['Region', 'City']).size().reset_index(name='Negative Reviews')
avg_rating = review.groupby(['Region', 'City'])['Rating'].mean().reset_index()

attention_df = total_reviews.merge(neg_reviews, on=['Region', 'City'], how='left').merge(avg_rating, on=['Region', 'City'])
attention_df['Negative Reviews'] = attention_df['Negative Reviews'].fillna(0)
attention_df['Negative Rate (%)'] = (attention_df['Negative Reviews'] / attention_df['Total Reviews']) * 100
attention_df['Rating'] = attention_df['Rating'].round(2)
attention_df['Score'] = attention_df['Negative Rate (%)'] * (4.5 - attention_df['Rating'])
top_attention = attention_df.sort_values('Score', ascending=False).head(10)


region_city_counts = top_attention['Region'].value_counts().reset_index()
region_city_counts.columns = ['Region', 'Cities Needing Attention']

fig_priority = px.bar(
    region_city_counts,
    x='Cities Needing Attention',
    y='Region',
    orientation='h',
    color='Region',
    color_discrete_map=region_colors
)


fig_priority.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    showlegend=False  # ← هذا هو السطر اللي يحذف legend
)

st.plotly_chart(fig_priority, use_container_width=True)

# ────────────────────────────────
# SECTION 4: REGION PRIORITY
# ────────────────────────────────
st.markdown("<h2>Cities Requiring Immediate Attention</h2>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<p style='text-align: center;'>
The chart ranks cities based on their <strong>Attention Score</strong>,
a metric that combines the proportion of negative reviews and low average ratings.
These cities may require urgent action to enhance visitor satisfaction.
</p>
""", unsafe_allow_html=True)

region_city_counts = top_attention['Region'].value_counts().reset_index()
region_city_counts.columns = ['Region', 'Cities Needing Attention']


fig_attention = px.bar(top_attention, x='Score', y='City', color='Region', orientation='h',
                       color_discrete_map=region_colors)
fig_attention.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig_attention, use_container_width=True)



# ────────────────────────────────
# SECTION 5: AVERAGE RATING BY REGION/TYPE
# ────────────────────────────────
region_type_ratings = review.groupby(["Region", "Place Type"])["Rating"].mean().reset_index()

st.markdown("<h2>Average Rating by Region and Place Type</h2>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<p style='text-align: center;'>
This chart compares the average ratings of different types of tourist places across Saudi regions.
It helps identify which types of places perform better in each region based on visitor feedback.
</p>
""", unsafe_allow_html=True)

fig3 = px.bar(
    region_type_ratings,
    x="Region",
    y="Rating",
    color="Place Type",
    barmode="group"
)
fig3.update_layout(
    xaxis_tickangle=-45,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)'
)
st.plotly_chart(fig3, use_container_width=True)
