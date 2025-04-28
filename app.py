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
    return pd.read_csv("notebooks/review_data.csv")

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

st.markdown("""
    <h2 style='text-align: center; margin-top: 20px;'>📊 Filtered Reviews and Sentiment Distribution</h2>
""", unsafe_allow_html=True)

# Create two columns: left for the table, right for the pie chart
col1, col2 = st.columns([2, 1])  # Wider column for the table

with col1:
    # Group by Place Name and calculate the average rating
    place_avg_rating = filtered.groupby(
        ['Region', 'City', 'Place Type', 'Place Name', 'Place Category']
    )['Rating'].mean().reset_index()

    # Round the average rating to 2 decimal places
    place_avg_rating['Rating'] = place_avg_rating['Rating'].round(2)

    # Display the dataframe
    st.dataframe(
        place_avg_rating[['Region', 'City', 'Place Type', 'Place Name', 'Place Category', 'Rating']],
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

# ───────────────────────────────────────────────
# SECTION 4: Cities That Might Need Ministry Attention (Smart Analysis + Cleaned)
# ───────────────────────────────────────────────

# Centered title
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
        <h2 style='text-align: center;'>🏙️ Cities That Might Need Ministry Attention</h2>
    """, unsafe_allow_html=True)

# Step 1: Calculate total reviews per city
total_reviews = filtered.groupby(['Region', 'City']).size().reset_index(name='Total Reviews')

# Step 2: Calculate negative reviews per city
neg_reviews = filtered[filtered['Sentiment Label'] == 'negative'].groupby(['Region', 'City']).size().reset_index(name='Negative Reviews')

# Step 3: Calculate average rating per city
avg_rating = filtered.groupby(['Region', 'City'])['Rating'].mean().reset_index()

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
