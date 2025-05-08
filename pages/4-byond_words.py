import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from gensim import corpora
from gensim.models.ldamodel import LdaModel
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
    return pd.read_csv("/Users/macbookpro/code/HayaAlsubie/Beyond_the_Stars/data/cleaned_reviews.csv")
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

# العنوان الرئيسي
st.markdown("""
    <div style='margin: 0 auto; width: 900px;'>
        <h2 style='text-align: center; color: black;'>Most Repeated Negative Words by City</h2>
""", unsafe_allow_html=True)

# فلتر المدينة
city_options = sorted(data["City"].dropna().unique())
selected_city = st.selectbox("📍 اختر المدينة", options=city_options)

# فلترة البيانات حسب المدينة والمراجعات السلبية الإنجليزية
filtered_data = data[
    (data["Reviewer Language"] == "en") &
    (data["Predicted Sentiment Label"] == "negative") &
    (data["City"] == selected_city) &
    data["cleaned_review"].notnull()
].copy()

# استخراج التوكينات
filtered_data["tokens"] = filtered_data["cleaned_review"].apply(clean_tokens)

# بناء نموذج LDA
tokens = filtered_data["tokens"]
dictionary = corpora.Dictionary(tokens)
corpus = [dictionary.doc2bow(text) for text in tokens]
lda_model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=5, passes=10, random_state=42)

# استخراج الكلمات المفتاحية
def extract_keywords(topics):
    words = []
    for topic in topics:
        _, content = topic
        words += re.findall(r'"(.*?)"', content)
    return words

all_keywords = extract_keywords(lda_model.print_topics())
word_counts = Counter(all_keywords).most_common(10)

# الرسم البياني بدون خلفية
if word_counts:
    words, counts = zip(*word_counts)
    fig, ax = plt.subplots()
    fig.patch.set_alpha(0.0)
    ax.set_facecolor('none')
    ax.barh(words, counts, color='#D16666')
    ax.set_title(f"Top Words in Negative Reviews - {selected_city}", fontsize=18, weight='bold')
    ax.set_xlabel("Frequency")
    ax.invert_yaxis()
    st.pyplot(fig)
else:
    st.info("لا توجد كلمات كافية للعرض.")

st.markdown("</div>", unsafe_allow_html=True)
