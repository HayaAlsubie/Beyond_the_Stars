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
# Compare Average Rating by Place Type
# ───────────────────────────────────────────────
type_ratings = review.groupby("Place Type")["Rating"].mean().sort_values(ascending=False).reset_index()

st.markdown("""
<div style='text-align: center; padding: 10px; background-color: rgba(0,0,0,0.5); border-radius: 10px; margin-top: 30px;'>
    <h2 style='color: white;'> Average Rating by Place Type</h2>
</div>
""", unsafe_allow_html=True)
st.dataframe(type_ratings)


# import matplotlib.pyplot as plt
# import seaborn as sns

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
type_sentiment = review.groupby(["Place Type", "Sentiment Label"]).size().unstack(fill_value=0)

st.markdown("""
<div style='text-align: center; padding: 10px; background-color: rgba(0,0,0,0.5); border-radius: 10px; margin-top: 30px;'>
    <h2 style='color: white;'> Sentiment Distribution by Place Type</h2>
</div>
""", unsafe_allow_html=True)
st.dataframe(type_sentiment)

region_type_ratings = (
    review.groupby(["Region", "Place Type"])["Rating"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)


st.markdown("""
<div style='text-align: center; padding: 10px; background-color: rgba(0,0,0,0.5); border-radius: 10px; margin-top: 30px;'>
    <h2 style='color: white;'> 📍Average Rating by Region and Place Type</h2>
</div>
""", unsafe_allow_html=True)
st.dataframe(region_type_ratings)
