import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
#!pip install arabic-reshaper python-bidi
import arabic_reshaper
from bidi.algorithm import get_display

nltk.download('vader_lexicon', quiet=True)

st.set_page_config(page_title="Tourism Review Dashboard", layout="wide")

# Centered main title
st.markdown("""
    <h1 style='text-align: center;'>🇸🇦 Saudi Tourism Review Analyzer</h1>
""", unsafe_allow_html=True)


# Load data
@st.cache_data
def load_data():
    return pd.read_csv("notebooks/review_data.csv")

review = load_data()

# ───────────────────────────────────────────────
# GLOBAL FILTERS (Updated: Region > City > Place Type > Place Name)
# ───────────────────────────────────────────────
st.sidebar.header("🔎 Filter Options")

# Filter by Region
regions = st.sidebar.multiselect("Select Region(s)", options=review["Region"].unique())
region_filtered = review[review["Region"].isin(regions)] if regions else review

# Filter by City
cities = st.sidebar.multiselect("Select City(s)", options=region_filtered["City"].unique())
city_filtered = region_filtered[region_filtered["City"].isin(cities)] if cities else region_filtered

# ✅ New: Filter by Place Type
place_types = st.sidebar.multiselect("Select Place Type(s)", options=city_filtered["Place Type"].unique())
type_filtered = city_filtered[city_filtered["Place Type"].isin(place_types)] if place_types else city_filtered

filtered = type_filtered


# ✅ Done button
done = st.sidebar.button("Done")


st.markdown("""
    <div style='text-align: center; background-color: #eaf4ff; padding: 10px; border-radius: 8px; color: #333;'>
        Explore the data by choosing filters on the left. Click <b>'Done'</b> to view insights! 🔍


    </div>
""", unsafe_allow_html=True)


# ───────────────────────────────────────────────
# SECTION 1 : Filtered Reviews + Sentiment Pie Chart
# ───────────────────────────────────────────────

st.markdown("""
    <h2 style='text-align: center; margin-top: 20px;'>📊 Filtered Reviews and Sentiment Distribution</h2>
""", unsafe_allow_html=True)

# Create two columns: left for the table, right for the pie chart
col1, col2 = st.columns([2, 1])  # Wider column for the table

with col1:
    # Display filtered review data
    st.dataframe(
        filtered[['Region', 'City', 'Place Type', 'Place Name', "Place Category", "Rating", "Sentiment Label"]],
        use_container_width=True,
        hide_index=True
    )

with col2:
    if not filtered.empty:
        # Prepare data for sentiment pie chart
        sentiment_counts = filtered["Sentiment Label"].value_counts()
        labels = sentiment_counts.index
        sizes = sentiment_counts.values
        colors = ['#66b3ff', '#ffcc99', '#ff9999']

        # Create pie chart with smaller size and font for balance
        fig, ax = plt.subplots(figsize=(2.5, 2.5), dpi=100)
        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labels,
            colors=colors,
            autopct='%1.1f%%',
            startangle=140,
            textprops={'fontsize': 7}
        )

        # Match label colors and adjust font
        for i, text in enumerate(texts):
            text.set_color(colors[i])
            text.set_fontsize(8)
            text.set_fontweight("bold")

        for atext in autotexts:
            atext.set_fontsize(7)

        ax.axis('equal')  # Keep the pie chart circular
        ax.set_title("Sentiment Distribution", fontsize=10)

        # Display the pie chart
        st.pyplot(fig)
    else:
        st.info("No data available for selected filters.")

st.markdown("<br><br>", unsafe_allow_html=True)


# ───────────────────────────────────────────────
# SECTION 2: Compare Sentiment Between Two Regions (Fixed Width)
# ───────────────────────────────────────────────

# Centered container with fixed width
st.markdown("""
    <div style='margin: 0 auto; width: 900px;'>
        <h2 style='text-align: center;'>📊 Compare Sentiment Distribution Between Two Regions</h2>
""", unsafe_allow_html=True)

region_1, region_2 = st.columns(2)

with region_1:
    selected_region_1 = st.selectbox("📍 Select First Region", options=review["Region"].unique(), key="region_1")
    region1_data = review[review["Region"] == selected_region_1]

with region_2:
    selected_region_2 = st.selectbox("📍 Select Second Region", options=review["Region"].unique(), key="region_2")
    region2_data = review[review["Region"] == selected_region_2]

charts_col1, charts_col2 = st.columns(2)

with charts_col1:
    st.subheader(f"📌 Sentiment in: {selected_region_1}")
    if not region1_data.empty:
        fig1, ax1 = plt.subplots(figsize=(4, 3), dpi=100)
        sns.countplot(data=region1_data, x="Sentiment Label", order=["positive", "neutral", "negative"], palette="crest", ax=ax1)
        ax1.set_title(selected_region_1, fontsize=10)
        ax1.set_xlabel("Sentiment")
        ax1.set_ylabel("Review Count")
        st.pyplot(fig1)
    else:
        st.info("No data available for this region.")

with charts_col2:
    st.subheader(f"📌 Sentiment in: {selected_region_2}")
    if not region2_data.empty:
        fig2, ax2 = plt.subplots(figsize=(4, 3), dpi=100)
        sns.countplot(data=region2_data, x="Sentiment Label", order=["positive", "neutral", "negative"], palette="flare", ax=ax2)
        ax2.set_title(selected_region_2, fontsize=10)
        ax2.set_xlabel("Sentiment")
        ax2.set_ylabel("Review Count")
        st.pyplot(fig2)
    else:
        st.info("No data available for this region.")

# Close fixed-width div
st.markdown("</div>", unsafe_allow_html=True)



# ───────────────────────────────────────────────
# SECTION 3: Ministry Insights
# ───────────────────────────────────────────────

# Top and bottom rated
place_ratings = filtered.groupby(['Region', 'City', 'Place Type', 'Place Name'])['Rating'].mean().reset_index()
top_places = place_ratings.sort_values(by='Rating', ascending=False).head(10)
worst_places = place_ratings.sort_values(by='Rating', ascending=True).head(10)

# Title centered
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
        <h2 style='text-align: center;'>🧠 Insights & Recommendations</h2>
    """, unsafe_allow_html=True)

# Display full-width side-by-side tables with spacing
col1, col2 = st.columns([1, 1], gap="medium")

with col1:
    st.subheader("🌟 Top 10 Rated Places")
    st.dataframe(top_places, use_container_width=True, hide_index=True)

with col2:
    st.subheader("⚠️ Bottom 10 Rated Places")
    st.dataframe(worst_places, use_container_width=True, hide_index=True)

# Attention-needed
neg_sentiment_counts = filtered[filtered['Sentiment Label'] == 'negative'].groupby(
    ['Region', 'City', 'Place Type', 'Place Name']).size().reset_index(name='Negative Reviews')
avg_ratings = filtered.groupby(['Region', 'City', 'Place Type', 'Place Name'])['Rating'].mean().reset_index()
attention_df = pd.merge(neg_sentiment_counts, avg_ratings, on=['Region', 'City', 'Place Type', 'Place Name'])
attention_needed = attention_df.sort_values(by='Negative Reviews', ascending=False).head(10)

st.markdown("## 🏙️ Cities That Might Need Ministry Attention")
st.dataframe(attention_needed, hide_index=True)

# Mismatches
filtered['Mismatch'] = filtered.apply(
    lambda row: 'Yes' if (row['compound'] < 0 and row['Rating'] >= 4.0) else 'No', axis=1)
mismatched_reviews = filtered[filtered['Mismatch'] == 'Yes'][[
    'Region', 'City', 'Place Type', 'Place Name', 'Rating', 'compound', 'Review Text'
]].head(10)

st.subheader("🚨 Suspected Rating-Sentiment Mismatches")
st.dataframe(mismatched_reviews, hide_index=True)

# ───────────────────────────────────────────────
# Compare Average Rating by Place Type
# ───────────────────────────────────────────────
type_ratings = filtered.groupby("Place Type")["Rating"].mean().sort_values(ascending=False).reset_index()

st.subheader("📊 Average Rating by Place Type")
st.dataframe(type_ratings)


import matplotlib.pyplot as plt
import seaborn as sns

# Chart for average rating by Place Type
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=type_ratings, x="Place Type", y="Rating", palette="viridis", ax=ax)
ax.set_title("📊 Average Rating by Place Type", fontsize=14)
ax.set_xlabel("Place Type")
ax.set_ylabel("Average Rating")
plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig)

# Optional: Add sentiment breakdown per type
type_sentiment = filtered.groupby(["Place Type", "Sentiment Label"]).size().unstack(fill_value=0)

st.subheader("😊 Sentiment Distribution by Place Type")
st.dataframe(type_sentiment)

region_type_ratings = (
    filtered.groupby(["Region", "Place Type"])["Rating"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

st.subheader("📍 Average Rating by Region and Place Type")
st.dataframe(region_type_ratings)
