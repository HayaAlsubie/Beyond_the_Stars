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
st.title("🇸🇦 Saudi Tourism Review Analyzer")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("review_data.csv")

review = load_data()

# ───────────────────────────────────────────────
# GLOBAL FILTERS (Apply Once to All Sections)
# ───────────────────────────────────────────────
st.sidebar.header("🔎 Filter Options")

regions = st.sidebar.multiselect("Select Region(s)", options=review["Region"].unique())
region_filtered = review[review["Region"].isin(regions)] if regions else review

cities = st.sidebar.multiselect("Select City(s)", options=region_filtered["City"].unique())
city_filtered = region_filtered[region_filtered["City"].isin(cities)] if cities else region_filtered

places = st.sidebar.multiselect("Select Place(s)", options=city_filtered["Place Name"].unique())
filtered = city_filtered[city_filtered["Place Name"].isin(places)] if places else city_filtered

# ───────────────────────────────────────────────
# SECTION 1: Filtered Review Data
# ───────────────────────────────────────────────
st.header("📊 Filtered Reviews")
st.subheader(f"Showing {len(filtered)} Reviews")
st.dataframe(filtered[["Region", "City", "Place Name", "Place Category", "Rating", "Sentiment Label"]])

# ───────────────────────────────────────────────
# SECTION 2: Sentiment Distribution
# ───────────────────────────────────────────────
st.header("📈 Sentiment Distribution (Filtered Data)")

def fix_arabic(text):
    """
    to make arabic names readable
    """
    try:
        reshaped_text = arabic_reshaper.reshape(text)
        return get_display(reshaped_text)
    except:
        return text
if not filtered.empty:
    fig, ax = plt.subplots()
    sns.countplot(data=filtered, x="Sentiment Label", order=["positive", "neutral", "negative"], palette="magma", ax=ax)
    ax.set_xlabel("Sentiment")
    ax.set_ylabel("Review Count")
    title_parts = []

    if regions:
        title_parts.append(f"Region(s): {', '.join(regions)}")
    if cities:
        title_parts.append(f"City(s): {', '.join(cities)}")
    if places:
        title_parts.append(f"Place(s): {', '.join(places)}")

    title_lines = ["Sentiment Distribution"]

    if regions:
        title_lines.append("Region: " + ", ".join(regions))
    if cities:
        title_lines.append("City: " + ", ".join(cities))
    if places:
        fixed_places = [fix_arabic(p) for p in places]
        title_lines.append("Place: " + ", ".join(fixed_places))


    formatted_title = "\n".join(title_lines)
    ax.set_title(formatted_title, fontsize=14)


    st.pyplot(fig)
else:
    st.info("No data available for selected filters.")

# ───────────────────────────────────────────────
# SECTION 3: Ministry Insights
# ───────────────────────────────────────────────
st.markdown("---")
st.header("🧠 Insights & Recommendations")

# Top and bottom rated
place_ratings = filtered.groupby(['Region', 'Place Name', 'City'])['Rating'].mean().reset_index()
top_places = place_ratings.sort_values(by='Rating', ascending=False).head(10)
worst_places = place_ratings.sort_values(by='Rating', ascending=True).head(10)

col1, col2 = st.columns(2)
with col1:
    st.subheader("🌟 Top 10 Rated Places")
    st.dataframe(top_places)
with col2:
    st.subheader("⚠️ Bottom 10 Rated Places")
    st.dataframe(worst_places)

# Attention-needed
neg_sentiment_counts = filtered[filtered['Sentiment Label'] == 'negative'].groupby(
    ['Region', 'Place Name', 'City']).size().reset_index(name='Negative Reviews')
avg_ratings = filtered.groupby(['Region', 'Place Name', 'City'])['Rating'].mean().reset_index()
attention_df = pd.merge(neg_sentiment_counts, avg_ratings, on=['Region', 'Place Name', 'City'])
attention_needed = attention_df.sort_values(by='Negative Reviews', ascending=False).head(10)

st.subheader("🔍 Places That Might Need Ministry Attention")
st.dataframe(attention_needed)

# Mismatches
filtered['Mismatch'] = filtered.apply(
    lambda row: 'Yes' if (row['compound'] < 0 and row['Rating'] >= 4.0) else 'No', axis=1)
mismatched_reviews = filtered[filtered['Mismatch'] == 'Yes'][[
    'Region', 'Place Name', 'City', 'Rating', 'compound', 'Review Text'
]].head(10)

st.subheader("🚨 Suspected Rating-Sentiment Mismatches")
st.dataframe(mismatched_reviews)

# ───────────────────────────────────────────────
# SECTION 4: Sentiment Tester
# ───────────────────────────────────────────────
with st.expander("✍️ Try Live Sentiment Analysis (Test a Review)", expanded=False):
    user_review = st.text_area("Write a review:")

    sid = SentimentIntensityAnalyzer()
    if user_review:
        sentiment_scores = sid.polarity_scores(user_review)
        compound = sentiment_scores["compound"]

        if compound >= 0.05:
            sentiment_label = "positive"
        elif compound <= -0.05:
            sentiment_label = "negative"
        else:
            sentiment_label = "neutral"

        st.markdown(f"**Predicted Sentiment:** `{sentiment_label}`")
        st.json(sentiment_scores)
