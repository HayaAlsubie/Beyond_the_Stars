import streamlit as st
import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
import seaborn as sns

# 🟢 إعداد الصفحة بلون الخلفية
st.set_page_config(page_title="Beyond Words", layout="wide")

# 🟣 تفعيل تنسيق الصفحة
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

# 🟡 تحميل البيانات والنماذج
df = pd.read_csv('pages/negative_reviews_w_clusters.csv')
lda_model = joblib.load('pages/lda_neg_tot.pkl')
kmeans_model = joblib.load('pages/kmeans_model.pkl')
vectorizer = joblib.load('pages/vectorizer.pkl')
feature_names = vectorizer.get_feature_names_out()

# 🧊 الفلاتر الجانبية
st.sidebar.title("🔍 Filters")
cities = df['City'].unique()
selected_city = st.sidebar.selectbox('Select City', sorted(cities))
place_types = df[df['City'] == selected_city]['Place Type'].unique()
selected_place_type = st.sidebar.selectbox('Select Place Type', sorted(place_types))

filtered_data = df[(df['City'] == selected_city) & (df['Place Type'] == selected_place_type)]

# 🟪 عنوان الصفحة
st.markdown("<h2 style='text-align: center; color:#153f2e'>Beyond Words</h2>", unsafe_allow_html=True)
st.markdown("""

""", unsafe_allow_html=True)

# 🧠 اختيار الموضوع
topic_numbers = list(range(lda_model.n_components))
selected_topic = st.selectbox('Select Topic to Explore', topic_numbers)

# 🧠 عرض الكلمات المفتاحية
top_word_indices = lda_model.components_[selected_topic].argsort()[::-1][:10]
top_words = [feature_names[i] for i in top_word_indices if i < len(feature_names)]
topic_df = pd.DataFrame(top_words, columns=["Keyword"])

# 🧩 تفسير الموضوع
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

keywords = top_words
interpretation = interpret_topic(keywords)

# ✅ عرض التفسير
st.markdown(f"<h4 style='color:#153f2e;'>🔍 Interpretation of Topic {selected_topic}</h4>", unsafe_allow_html=True)
st.markdown(interpretation)

# ✅ عرض كلمات الموضوع - رسم دائري بدون خلفية
st.markdown("<h4 style='color:#153f2e;'>📌 Top Keywords</h4>", unsafe_allow_html=True)
fig1, ax1 = plt.subplots(figsize=(6, 6), facecolor='#e6ebe0')
ax1.pie([1] * len(topic_df), labels=topic_df['Keyword'], autopct='%1.1f%%',
        startangle=140, colors=sns.color_palette("Purples_r"))
ax1.set_title("")
fig1.patch.set_facecolor('#e6ebe0')
st.pyplot(fig1)

# 🧠 Insights
st.markdown("<h4 style='color:#153f2e;'>✨ Key Insights</h4>", unsafe_allow_html=True)
st.markdown("""
- LDA modeling groups similar complaints together, making patterns easy to spot.
- Topics often relate to specific service problems like **delays**, **cleanliness**, or **staff behavior**.
- This allows tourism authorities to focus improvements on the most common pain points per city and business type.
""")

# 💡 Recommendations
st.markdown("<h4 style='color:#153f2e;'>💡 Recommendations</h4>", unsafe_allow_html=True)
st.markdown(f"""
Here are suggested improvements for Topic **{selected_topic}** based on its top keywords:

- **Improve Staff Training:** If keywords include 'rude', 'staff', 'service'.
- **Enhance Cleanliness Protocols:** If keywords include 'dirty', 'bathroom', 'clean'.
- **Streamline Check-in/Check-out Processes:** If you see 'delay', 'wait', 'slow'.
- **Better Communication with Guests:** For keywords like 'no response', 'not helpful'.

Customize actions based on the dominant issue in each topic to better meet visitor expectations.
""")
