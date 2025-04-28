import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data
def load_data():
    return pd.read_csv("notebooks/review_data.csv")

review = load_data()


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
    region1_place_types = st.multiselect(
        "Select Place Type(s) for Region 1",
        options=review[review["Region"] == selected_region_1]["Place Type"].unique(),
        key="region1_place_types"
    )
    region1_data = review[(review["Region"] == selected_region_1) &
                          (review["Place Type"].isin(region1_place_types))] if region1_place_types else \
                          review[review["Region"] == selected_region_1]

with region_2:
    selected_region_2 = st.selectbox("📍 Select Second Region", options=review["Region"].unique(), key="region_2")
    region2_place_types = st.multiselect(
        "Select Place Type(s) for Region 2",
        options=review[review["Region"] == selected_region_2]["Place Type"].unique(),
        key="region2_place_types"
    )
    region2_data = review[(review["Region"] == selected_region_2) &
                          (review["Place Type"].isin(region2_place_types))] if region2_place_types else \
                          review[review["Region"] == selected_region_2]



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
