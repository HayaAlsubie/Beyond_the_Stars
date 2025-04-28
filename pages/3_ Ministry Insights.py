import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# لو تحتاجين تحميل الداتا مرة ثانية
@st.cache_data
def load_data():
    return pd.read_csv("notebooks/review_data.csv")

review = load_data()


# ───────────────────────────────────────────────
# SECTION 3: Ministry Insights
# ───────────────────────────────────────────────

# Top and bottom rated
place_ratings = review.groupby(['Region', 'City', 'Place Type', 'Place Name'])['Rating'].mean().reset_index()
top_places = place_ratings.sort_values(by='Rating', ascending=False).head(10)
worst_places = place_ratings.sort_values(by='Rating', ascending=True).head(10)

# Title centered
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
  st.markdown("""
    <div style='text-align: center; padding: 10px; background-color: rgba(0,0,0,0.5); border-radius: 10px; margin-top: 30px;'>
        <h2 style='color: white;'> Insights & Recommendations</h2>
    </div>
    """, unsafe_allow_html=True)

# Display full-width side-by-side tables with spacing
col1, col2 = st.columns([1, 1], gap="medium")

with col1:
    st.markdown("""
    <div style='text-align: center; padding: 10px; background-color: rgba(0,0,0,0.5); border-radius: 10px; margin-top: 30px;'>
        <h2 style='color: white;'>🌟 Top 10 Rated Places</h2>
    </div>
    """, unsafe_allow_html=True)
    st.dataframe(top_places, use_container_width=True, hide_index=True)

with col2:
    st.markdown("""
    <div style='text-align: center; padding: 10px; background-color: rgba(0,0,0,0.5); border-radius: 10px; margin-top: 30px;'>
        <h2 style='color: white;'>⚠️ Bottom 10 Rated Places</h2>
    </div>
    """, unsafe_allow_html=True)
    st.dataframe(worst_places, use_container_width=True, hide_index=True)





# ───────────────────────────────────────────────
# SECTION 4: Cities That Might Need Ministry Attention (Smart Analysis + Cleaned)
# ───────────────────────────────────────────────

# Centered title
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
   st.markdown("""
    <div style='text-align: center; padding: 10px; background-color: rgba(0,0,0,0.5); border-radius: 10px; margin-top: 30px;'>
        <h2 style='color: white;'> Cities That Might Need Ministry Attention</h2>
    </div>
    """, unsafe_allow_html=True)

# Step 1: Calculate total reviews per city
total_reviews = review.groupby(['Region', 'City']).size().reset_index(name='Total Reviews')

# Step 2: Calculate negative reviews per city
neg_reviews = review[review['Sentiment Label'] == 'negative'].groupby(['Region', 'City']).size().reset_index(name='Negative Reviews')

# Step 3: Calculate average rating per city
avg_rating = review.groupby(['Region', 'City'])['Rating'].mean().reset_index()

# Step 4: Merge all together
city_summary = total_reviews.merge(neg_reviews, on=['Region', 'City'], how='left').merge(avg_rating, on=['Region', 'City'])
city_summary['Negative Reviews'] = city_summary['Negative Reviews'].fillna(0)  # Fill cities with no negatives
city_summary['Negative Rate (%)'] = (city_summary['Negative Reviews'] / city_summary['Total Reviews']) * 100

# Step 5: Filter cities that really need attention
attention_needed = city_summary[
    (city_summary['Negative Rate (%)'] >= 30) &
    (city_summary['Rating'] < 4.0)
].sort_values(by='Negative Rate (%)', ascending=False)

# Step 6: Round percentages and ratings
attention_needed['Negative Rate (%)'] = attention_needed['Negative Rate (%)'].round(1)
attention_needed['Rating'] = attention_needed['Rating'].round(2)

# Step 7: Reorder columns for better view
attention_needed = attention_needed[['Region', 'City', 'Total Reviews', 'Negative Reviews', 'Negative Rate (%)', 'Rating']]

# Display nicely centered
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.dataframe(attention_needed, use_container_width=True, hide_index=True)

# Add space after the section
st.markdown("<br><br>", unsafe_allow_html=True)
