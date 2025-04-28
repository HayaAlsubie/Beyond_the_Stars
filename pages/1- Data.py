import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import nltk




nltk.download('vader_lexicon', quiet=True)

st.set_page_config(page_title="Tourism Review Dashboard", layout="wide")


# Centered main title
st.markdown("""
    <h1 style='text-align: center;'>🇸🇦Saudi Tourism Review Analyzer</h1>
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



st.markdown("""
    <div style='text-align: center; background-color: #eaf4ff; padding: 10px; border-radius: 8px; color: #333;'>
        Explore the data by choosing filters on the left to view insights!


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
