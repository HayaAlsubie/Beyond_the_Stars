import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from nltk.corpus import stopwords
import nltk
import re
from collections import Counter

# تحميل stopwords
try:
    stopwords.words('english')
except LookupError:
    nltk.download('stopwords')

# تحميل البيانات
@st.cache_data
def load_data():
    return pd.read_csv("data/cleaned_reviews.csv")
data = load_data()

# تنظيف وتوكينات
english_stopwords = set(stopwords.words('english'))
custom_exclude = {
    "like", "us", "time", "experience", "recommend", "didnt", "dont",
    "one", "even", "go", "rooms", "wasnt", "stay", "available", "alula",
    "good","abha","city","also","ac","nothing","sit","get","al","water","bin","hail"
    ,"ive","average","two","give", "asked","much","night","really","came","tasty",
    "baha","rice","overall","fish", "got","would", "professional", "last", "please", "chicken"
    , "makkah", "table", "top", "said", "starbucks", "almaa", "going", "day", "working", "tabuk", "railway",
    "umluj", "pm", "sea", "got","ever","mark","breakfast","unfortunately","haram"
    , "another", "rijal", "mandhi", "small", "etc", "doesnt", "days", "cup", "cups", "size", "branch", "foodgood"
    , "shuttle", "burger", "made", "know", "making", "inside", "biryani", "open", "told", "want", "raw", "jeddah",
    "try", "take","red","taif","mecca","jumeirah","shawarma","u","minutes","see","way","policy","theres","key","soap"
    ,"never","tea","yanbu","pizza","salad","saudi","qishlah","still","couldnt","first","musaad","madinah"
    }
def clean_tokens(text):
    tokens = str(text).lower().split()
    return [word for word in tokens if word not in english_stopwords and word not in custom_exclude and word.isalpha()]

# إعداد صفحة Streamlit
st.set_page_config(page_title="Beyond Words", layout="wide")

# تنسيق الصفحة مثل صفحة Compare
st.markdown("""
    <style>
    .stApp { background-color: #e6ebe0; }

    header[data-testid="stHeader"] {
        background-color: #e6ebe0;
    }

    section[data-testid="stSidebar"] {
        background-color: #153f2e;
    }
    section[data-testid="stSidebar"] * {
        color: #e6ebe0;
    }
    [data-testid="stSidebarNav"] ul li a {
        color: #e6ebe0;
        font-weight: 500;
    }
    [data-testid="stSidebarNav"] ul li a[aria-current="page"] {
        color: #CBA135;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# العنوان + الفلتر + الرسم في عرض موحد

st.markdown("""
    <div style='margin: 0 auto; width: 700px; text-align: center;'>
        <h2 style='color: black;'>Top Words in Negative Reviews</h2>
""", unsafe_allow_html=True)

# مسافة بين العنوان والفلاتر
st.markdown("<br>", unsafe_allow_html=True)

# فلتر المدينة
city_options = sorted(data["City"].dropna().unique())
selected_city = st.selectbox("Select a City:", options=city_options)

# الجملة التوضيحية بعد ما نختار المدينة
st.markdown(f"<p style='text-align:center;'>This chart highlights the most common negative keywords used by tourists in <strong>{selected_city}</strong>. These insights help identify areas for service improvement.</p>", unsafe_allow_html=True)

# فلترة البيانات حسب المدينة والمراجعات السلبية
filtered_data = data[
    (data["Reviewer Language"] == "en") &
    (data["Predicted Sentiment Label"] == "negative") &
    (data["City"] == selected_city) &
    data["cleaned_review"].notnull()
].copy()

# استخراج التوكينات
filtered_data["tokens"] = filtered_data["cleaned_review"].apply(clean_tokens)


# بناء نموذج LDA باستخدام sklearn
documents = filtered_data["tokens"].apply(lambda x: ' '.join(x)).tolist()

vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
doc_term_matrix = vectorizer.fit_transform(documents)

lda_model = LatentDirichletAllocation(n_components=5, random_state=42)
lda_model.fit(doc_term_matrix)

# استخراج الكلمات
words = vectorizer.get_feature_names_out()
all_keywords = []
for topic in lda_model.components_:
    top_words = [words[i] for i in topic.argsort()[-10:]]
    all_keywords.extend(top_words)


# عرض الرسم البياني في نفس الكتلة
if all_keywords:
    word_counts = Counter(all_keywords).most_common(10)
    words, counts = zip(*word_counts)
    fig, ax = plt.subplots(figsize=(7, 5))
    fig.patch.set_alpha(0.0)
    ax.set_facecolor('none')
    ax.barh(words, counts, color='#D16666')
    ax.set_title("")  # حذف العنوان من داخل الشكل
    ax.set_xlabel("Frequency")
    ax.invert_yaxis()
    st.pyplot(fig)
else:
    st.info("No negative reviews available for this city in English.")

st.markdown("</div>", unsafe_allow_html=True)
