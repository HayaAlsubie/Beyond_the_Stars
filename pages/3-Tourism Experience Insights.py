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
    return pd.read_csv("notebooks/review_data.csv")

review = load_data()



# Rename long Arabic place names to shorter English ones
review['Place Name'] = review['Place Name'].replace({
    "واحة عبدالله أحمد الزامل للعلوم": "Science Oasis",
    "شاليهات روزانه الترفيهية": "Rozana Chalets",
    "مطعم زاوية حكاية": "Hekaya Restaurant",
    "فندق نارس البخاري": "Nars Hotel",
    "مخيم بِنتر": "Winter Camp",
    "شركة تنظيف منازل بالقطيف تنظيف مفروشات غسيل سجاد تنظيف كنب القطيف": "Qatif Mall.",
    "بيت الطيبين": "AlTayyib House"
})


# ────────────────────────────────
# SECTION 1: PAGE TITLE
# ────────────────────────────────
st.markdown("<h1 style='text-align: center;'>Ministry Insights from Visitor Reviews</h1>", unsafe_allow_html=True)

# ────────────────────────────────
# SECTION 2: TOP & BOTTOM RATED
# ────────────────────────────────
place_ratings = review.groupby(['Region', 'City', 'Place Type', 'Place Name'])['Rating'].mean().reset_index()
top_places = place_ratings.sort_values(by='Rating', ascending=False).head(10)
worst_places = place_ratings.sort_values(by='Rating', ascending=True).head(10)

st.markdown("<h2>Top 10 Rated Places</h2>", unsafe_allow_html=True)
fig_top = px.bar(top_places, x='Place Name', y='Rating', color='Region',
                 color_discrete_map=region_colors)
fig_top.update_layout(xaxis_tickangle=-45, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig_top, use_container_width=True)

st.markdown("<h2>Bottom 10 Rated Places</h2>", unsafe_allow_html=True)
fig_bottom = px.bar(worst_places, x='Place Name', y='Rating', color='Region',
                    color_discrete_map=region_colors)
fig_bottom.update_layout(xaxis_tickangle=-45, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig_bottom, use_container_width=True)

# ────────────────────────────────
# SECTION 3: AVG RATING BY TYPE
# ────────────────────────────────
type_ratings = review.groupby("Place Type")["Rating"].mean().sort_values(ascending=False).reset_index()

st.markdown("<h2>Average Rating by Place Type</h2>", unsafe_allow_html=True)
fig1 = px.bar(type_ratings, x="Place Type", y="Rating", color="Rating", color_continuous_scale="Aggrnyl")
fig1.update_layout(xaxis_tickangle=-45, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig1, use_container_width=True)

# ────────────────────────────────
# SECTION 4: SENTIMENT DISTRIBUTION
# ────────────────────────────────
type_sentiment = review.groupby(["Place Type", "Sentiment Label"]).size().reset_index(name="Count")

st.markdown("<h2>Sentiment Distribution by Place Type</h2>", unsafe_allow_html=True)
fig2 = px.bar(
    type_sentiment,
    x="Place Type",
    y="Count",
    color="Sentiment Label",
    barmode="stack",
    color_discrete_map=sentiment_colors
)
fig2.update_layout(xaxis_tickangle=-45, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig2, use_container_width=True)

# ────────────────────────────────
# SECTION 5: RATING BY REGION/TYPE
# ────────────────────────────────
region_type_ratings = review.groupby(["Region", "Place Type"])["Rating"].mean().reset_index()

st.markdown("<h2>Average Rating by Region and Place Type</h2>", unsafe_allow_html=True)
fig3 = px.bar(region_type_ratings, x="Region", y="Rating", color="Place Type", barmode="group")
fig3.update_layout(xaxis_tickangle=-45, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig3, use_container_width=True)

# ────────────────────────────────
# SECTION 6: CITIES NEEDING ATTENTION
# ────────────────────────────────
st.markdown("<h2>Cities That Might Need Ministry Attention</h2>", unsafe_allow_html=True)
st.markdown("""
The **Attention Score** helps prioritize cities that may need urgent service improvements based on review patterns.

**Formula:**

**Attention Score = Negative Review Rate × (4.5 − Average Rating)**
""")

total_reviews = review.groupby(['Region', 'City']).size().reset_index(name='Total Reviews')
neg_reviews = review[review['Sentiment Label'] == 'negative'].groupby(['Region', 'City']).size().reset_index(name='Negative Reviews')
avg_rating = review.groupby(['Region', 'City'])['Rating'].mean().reset_index()

attention_df = total_reviews.merge(neg_reviews, on=['Region', 'City'], how='left').merge(avg_rating, on=['Region', 'City'])
attention_df['Negative Reviews'] = attention_df['Negative Reviews'].fillna(0)
attention_df['Negative Rate (%)'] = (attention_df['Negative Reviews'] / attention_df['Total Reviews']) * 100
attention_df['Rating'] = attention_df['Rating'].round(2)
attention_df['Score'] = attention_df['Negative Rate (%)'] * (4.5 - attention_df['Rating'])
top_attention = attention_df.sort_values('Score', ascending=False).head(10)

fig_attention = px.bar(top_attention, x='Score', y='City', color='Region', orientation='h',
                       color_discrete_map=region_colors)
fig_attention.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig_attention, use_container_width=True)

# ────────────────────────────────
# SECTION 7: REGION PRIORITY
# ────────────────────────────────
st.markdown("<h2>Regions with Most Concerning Cities</h2>", unsafe_allow_html=True)
region_city_counts = top_attention['Region'].value_counts().reset_index()
region_city_counts.columns = ['Region', 'Cities Needing Attention']

fig_priority = px.bar(region_city_counts, x='Cities Needing Attention', y='Region', orientation='h',
                      color='Region', color_discrete_map=region_colors)
fig_priority.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig_priority, use_container_width=True)
