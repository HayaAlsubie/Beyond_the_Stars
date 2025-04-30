import streamlit as st
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
import seaborn as sns


st.set_page_config(page_title="Beyond the Stars", layout="wide")

st.markdown("<h1 style='color:#800040;'> Beyond Words</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='color:#404040;'>Insights on Poorly Reviewed Businesses</h3>", unsafe_allow_html=True)

df = pd.read_csv('pages/negative_reviews_w_clusters.csv')
lda_model = joblib.load('pages/lda_neg_tot.pkl')
kmeans_model = joblib.load('pages/kmeans_model.pkl')
vectorizer = joblib.load('pages/vectorizer.pkl')
feature_names = vectorizer.get_feature_names_out()

df = df.drop(columns=['Sentiment Label', 'Place Category', 'Review Text', 'Reviewer Language', 'neg', 'neu', 'pos', 'compound'])

st.sidebar.title("Filters")
cities = df['City'].unique()
selected_city = st.sidebar.selectbox('Select City', sorted(cities))
place_types = df[df['City'] == selected_city]['Place Type'].unique()
selected_place_type = st.sidebar.selectbox('Select Place Type', sorted(place_types))

filtered_data = df[(df['City'] == selected_city) & (df['Place Type'] == selected_place_type)]

st.markdown(f"<h4 style='color:#800040;'>📌 Focus: Negative Reviews for {selected_place_type} in {selected_city}</h4>", unsafe_allow_html=True)
st.dataframe(filtered_data[['Cleaned Review']], height=200)

# LDA Topic Modeling
st.markdown("<h3 style='color:#660066;'>🔍 Topic Modeling using LDA</h3>", unsafe_allow_html=True)
st.markdown("""
Topics are clusters of frequent words found in negative reviews.
They reveal common concerns, helping us understand what frustrates customers the most.
""")

topic_numbers = list(range(lda_model.n_components))
selected_topic = st.selectbox('Select Topic to Explore', topic_numbers)





# Top keywords for selected topic
top_word_indices = lda_model.components_[selected_topic].argsort()[::-1][:10]
top_words = [feature_names[i] for i in top_word_indices if i < len(feature_names)]
topic_df = pd.DataFrame(top_words, columns=["Keyword"])



# Interpretation of Topic - Move this up
def interpret_topic(keywords):
    interpretation = f"Topic based on keywords: {', '.join(keywords)}. "

    if 'slow' in keywords or 'wait' in keywords:
        interpretation += "It seems that customers are complaining about delays or slow service."
    if 'tasted' in keywords or 'food' in keywords:
        interpretation += "There could be concerns regarding the quality of food or taste."
    if 'cashier' in keywords or 'service' in keywords:
        interpretation += "Issues with service and cashier experience seem to be mentioned frequently."
    if 'improvements' in keywords:
        interpretation += "Customers are asking for improvements in overall service or quality."

    return interpretation

# Interpret the selected topic - Display interpretation first
keywords = top_words
interpretation = interpret_topic(keywords)
st.markdown(f"#### 🔎 Interpretation of Topic {selected_topic}") #selected topic before
st.markdown(interpretation)

# Topic Keywords - Pie Chart (without Importance)
st.markdown("#### 📊 Topic Keywords")
fig1, ax1 = plt.subplots(figsize=(6, 6))
print(" / ".join(list(topic_df['Keyword'])))
ax1.pie([1] * len(topic_df), labels=topic_df['Keyword'] , autopct='%1.1f%%', startangle=140, colors=sns.color_palette("Purples_r"))
ax1.set_title(f"Top Keywords for Topic {selected_topic}") #sqme
st.pyplot(fig1)

# Topic Distribution - Pie Chart
st.markdown("####  Distribution of Topics")

topic_counts = filtered_data['Topic'].value_counts().sort_index()
fig2, ax2 = plt.subplots(figsize=(6, 6))
ax2.pie(topic_counts.values, labels=topic_counts.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("magma"))
ax2.set_title("Review Count per Topic")
st.pyplot(fig2)

# Key insights and recommendations
st.markdown("### ✨ Key Insights")
st.markdown("""
- LDA modeling groups similar complaints together, making patterns easy to spot.
- Topics often relate to specific service problems like **delays**, **cleanliness**, or **staff behavior**.
- This allows tourism authorities to focus improvements on the most common pain points per city and business type.
""")

st.markdown("### 💡 Recommendations")
st.markdown(f"""
Here are suggested improvements for Topic **{selected_topic}** based on its top keywords:

- **Improve Staff Training:** If keywords include 'rude', 'staff', 'service'.
- **Enhance Cleanliness Protocols:** If keywords include 'dirty', 'bathroom', 'clean'.
- **Streamline Check-in/Check-out Processes:** If you see 'delay', 'wait', 'slow'.
- **Better Communication with Guests:** For keywords like 'no response', 'not helpful'.

Customize actions based on the dominant issue in each topic to better meet visitor expectations.
""")
