import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
from collections import Counter

# ───────────────────────────────────────────────
# PAGE CONFIG & STYLING
# ───────────────────────────────────────────────
st.set_page_config(
    page_title="Tourism Experience Insights",
    layout="wide"
)

st.markdown("""
    <style>
        body {
            background-color: #F0F0F5;
        }
        .block-container {
            padding: 2rem 3rem;
        }
        h1 {
            color: #007A3D;
            font-size: 2.4rem;
        }
        h2 {
            color: #00AEEF;
            font-size: 1.8rem;
            margin-top: 2rem;
        }
        h3, .stMarkdown h3 {
            color: #7F3F98;
            margin-top: 1.5rem;
        }
        .stDataFrame thead tr th {
            background-color: #00AEEF;
            color: white;
        }
        .st-df {
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid #ccc;
        }
        hr {
            border: 1px solid #CBA135;
            margin-top: 2rem;
            margin-bottom: 2rem;
        }
        .stMarkdown {
            font-size: 1.05rem;
        }
    </style>
""", unsafe_allow_html=True)

# ───────────────────────────────────────────────
# LOAD DATA
# ───────────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_csv("notebooks/review_data.csv")

review = load_data()

# ───────────────────────────────────────────────
# SECTION 1: Top & Bottom Rated Places
# ───────────────────────────────────────────────
st.markdown("""<h1 style='text-align: center;'> Ministry Insights from Visitor Reviews</h1>""", unsafe_allow_html=True)
st.markdown("This dashboard summarizes visitor feedback across Saudi Arabia to help the Ministry identify strengths, weaknesses, and opportunities for improvement.")

st.markdown("""<h2>⭐ Top vs. ⚠️ Bottom Rated Places</h2>""", unsafe_allow_html=True)
place_ratings = review.groupby(['Region', 'City', 'Place Type', 'Place Name'])['Rating'].mean().reset_index()
top_places = place_ratings.sort_values(by='Rating', ascending=False).head(10)
worst_places = place_ratings.sort_values(by='Rating', ascending=True).head(10)

col1, col2 = st.columns(2)
with col1:
    st.markdown("#### 🌟 Top 10 Rated Places")
    st.dataframe(top_places, use_container_width=True, hide_index=True)
with col2:
    st.markdown("#### ⚠️ Bottom 10 Rated Places")
    st.dataframe(worst_places, use_container_width=True, hide_index=True)

# ───────────────────────────────────────────────
# SECTION 2: Cities That Might Need Ministry Attention
# ───────────────────────────────────────────────
st.markdown("""<h2>🚨 Cities That Might Need Ministry Attention</h2>""", unsafe_allow_html=True)
st.markdown("""
These are the top 10 cities with the most concerning combination of high negative review rates and low average ratings.
The **Attention Score** is calculated as: `Negative Rate × (4.5 − Average Rating)`.
""")

total_reviews = review.groupby(['Region', 'City']).size().reset_index(name='Total Reviews')
neg_reviews = review[review['Sentiment Label'] == 'negative'].groupby(['Region', 'City']).size().reset_index(name='Negative Reviews')
avg_rating = review.groupby(['Region', 'City'])['Rating'].mean().reset_index()

attention_df = total_reviews.merge(neg_reviews, on=['Region', 'City'], how='left').merge(avg_rating, on=['Region', 'City'])
attention_df['Negative Reviews'] = attention_df['Negative Reviews'].fillna(0)
attention_df['Negative Rate (%)'] = (attention_df['Negative Reviews'] / attention_df['Total Reviews']) * 100
attention_df['Negative Rate (%)'] = attention_df['Negative Rate (%)'].round(1)
attention_df['Rating'] = attention_df['Rating'].round(2)
attention_df['Score'] = attention_df['Negative Rate (%)'] * (4.5 - attention_df['Rating'])

top_cities = attention_df.sort_values('Score', ascending=False).head(10)

fig, ax = plt.subplots(figsize=(10, 6))
custom_palette = ["#007A3D", "#00AEEF", "#7F3F98", "#CBA135", "#A1CDA8"]
sns.barplot(y="City", x="Score", data=top_cities, palette=custom_palette, ax=ax)
ax.set_xlabel("Attention Score (Higher = More Concerning)")
ax.set_ylabel("City")
ax.set_title("Top 10 Cities by Attention Score")
st.pyplot(fig)

# ───────────────────────────────────────────────
# SECTION 3: Complaint Tags by City
# ───────────────────────────────────────────────
st.markdown("""<h2>📌 Root Causes by City (Complaint Tags)</h2>""", unsafe_allow_html=True)
st.markdown("This table shows the top 3 complaint keywords in each city and translates them into categorized tags.")

neg_reviews_text = review[review['Sentiment Label'] == 'negative'][['City', 'Review Text']].dropna()

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    tokens = text.split()
    stop_words = set(["the", "and", "was", "were", "are", "with", "very", "but", "not", "for", "this", "that", "they", "too", "had", "have", "has", "just", "you", "from", "all", "out", "about", "our", "there", "their", "been", "after", "place", "restaurant", "hotel", "visit", "service"])
    return [word for word in tokens if word not in stop_words and len(word) > 2]

neg_reviews_text['Tokens'] = neg_reviews_text['Review Text'].apply(clean_text)
city_complaints = (
    neg_reviews_text.groupby('City')['Tokens']
    .sum()
    .apply(lambda x: Counter(x).most_common(3))
    .reset_index()
    .rename(columns={'Tokens': 'Top Complaints'})
)

keyword_map = {
    "room": "🛏️ Accommodation", "rooms": "🛏️ Accommodation",
    "staff": "🤝 Service", "rude": "🤝 Service", "attitude": "🤝 Service",
    "food": "🍽️ Food",
    "dirty": "🧼 Cleanliness", "clean": "🧼 Cleanliness", "cleanliness": "🧼 Cleanliness",
    "price": "💰 Affordability", "expensive": "💰 Affordability",
    "wait": "⏱️ Efficiency", "slow": "⏱️ Efficiency",
    "noise": "🔇 Environment", "parking": "🅿️ Accessibility"
}

def map_keywords_to_tags(complaints):
    tags = set()
    for word, _ in complaints:
        if word in keyword_map:
            tags.add(keyword_map[word])
    return ' • '.join(sorted(tags))

city_complaints['Top Keywords'] = city_complaints['Top Complaints'].apply(lambda x: ', '.join([w for w, _ in x]))
city_complaints['Insight Tags'] = city_complaints['Top Complaints'].apply(map_keywords_to_tags)

final_table = city_complaints[['City', 'Top Keywords', 'Insight Tags']]
st.dataframe(final_table, use_container_width=True, hide_index=True)

# ───────────────────────────────────────────────
# SECTION 4: Regional Priority Summary
# ───────────────────────────────────────────────
st.markdown("""<h2>📍 Regional Priority Based on Problematic Cities</h2>""", unsafe_allow_html=True)
st.markdown("""
This chart shows how many of the top 10 most concerning cities (based on review negativity and rating) fall into each region.
Regions with more flagged cities may require more urgent or extensive Ministry action.
""")

region_city_counts = top_cities['Region'].value_counts().reset_index()
region_city_counts.columns = ['Region', 'Cities Needing Attention']
region_city_counts = region_city_counts.sort_values(by='Cities Needing Attention', ascending=False)

fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x='Cities Needing Attention', y='Region', data=region_city_counts, palette=custom_palette, ax=ax)
ax.set_title("Regions by Number of Concerning Cities")
ax.set_xlabel("Number of Cities in Top 10 Needing Attention")
ax.set_ylabel("Region")
st.pyplot(fig)
