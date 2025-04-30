import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import nltk

# إعداد الصفحة
st.set_page_config(page_title="Tourism Review Dashboard", layout="wide")

# 🌿 تنسيق الخلفية والشريط الجانبي بنفس introduction
st.markdown("""
<style>
/* خلفية الصفحة */
.stApp {
    background-color: #e6ebe0;
    color: black;
}
/* الشريط العلوي */
header[data-testid="stHeader"] {
    background-color: #e6ebe0 !important;
}
/* الشريط الجانبي */
section[data-testid="stSidebar"] {
    background-color: #153f2e !important;
}
section[data-testid="stSidebar"] * {
    color: #e6ebe0 !important;
}
/* أسماء الصفحات */
[data-testid="stSidebarNav"] ul li a {
    color: #e6ebe0 !important;
    font-weight: 500;
}
/* الصفحة الحالية */
[data-testid="stSidebarNav"] ul li a[aria-current="page"] {
    color: #CBA135 !important;
    font-weight: bold;
}

/* ✅ مربعات الفلتر بلون زيتوني */
section[data-testid="stSidebar"] .stSelectbox {
    background-color: #e6ebe0 !important;
    border-radius: 8px;
}
section[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] {
    background-color: #e6ebe0 !important;

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* تغيير لون عنوان الفلتر داخل الشريط الجانبي */
section[data-testid="stSidebar"] h3 {
    color: #BFA76F !important;
}
</style>
""", unsafe_allow_html=True)


# تحميل قاموس المشاعر
nltk.download('vader_lexicon', quiet=True)

# تحميل البيانات
@st.cache_data
def load_data():
    return pd.read_csv("notebooks/review_data.csv")
review = load_data()

# العنوان الرئيسي + وصف الصفحة
st.markdown("""
<h1 style='text-align: center; font-size: 42px; color: black; font-family: "Segoe UI", sans-serif; margin-bottom: 5px;'>
    Saudi Tourism Review Analyzer
</h1>

""", unsafe_allow_html=True)

# ───────────────────────────────────────────────
# GLOBAL FILTERS
# ───────────────────────────────────────────────
st.sidebar.markdown("<h3 style='color: #BFA76F;'>🔍 Filter Options</h3>", unsafe_allow_html=True)


regions = st.sidebar.multiselect("Select Region(s)", options=review["Region"].unique())
region_filtered = review[review["Region"].isin(regions)] if regions else review

cities = st.sidebar.multiselect("Select City(s)", options=region_filtered["City"].unique())
city_filtered = region_filtered[region_filtered["City"].isin(cities)] if cities else region_filtered

place_types = st.sidebar.multiselect("Select Place Type(s)", options=city_filtered["Place Type"].unique())
type_filtered = city_filtered[city_filtered["Place Type"].isin(place_types)] if place_types else city_filtered

filtered = type_filtered

# رسالة صغيرة
st.markdown("""
<div style='text-align: center; background-color: #f8f8f8; padding: 10px; border-radius: 8px; margin-top: 20px;'>
    Use the filters on the left to explore customized insights.
</div>
""", unsafe_allow_html=True)

# ───────────────────────────────────────────────
# SECTION 1: Filtered Reviews + Pie Chart
# ───────────────────────────────────────────────
st.markdown("""
<h2 style='color: black; text-align: center; margin-top: 30px;'> Filtered Reviews and Sentiment Distribution</h2>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

# ✅ جدول بتنسيق أنيق
def render_styled_table(df):
    styled_table = df.to_html(classes='styled-table', index=False, escape=False)
    st.markdown("""
    <style>
        .styled-table-wrapper {
            max-width: 700px;
            margin-left: auto;
            margin-right: auto;
            overflow-x: auto;
            overflow-y: auto;
            max-height: 450px;
            margin-top: 35px;
        }
        .styled-table {
            border-collapse: collapse;
            font-size: 15px;
            font-family: 'Segoe UI', sans-serif;
            width: 100%;
            background-color: white;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.05);
        }
        .styled-table thead tr {
            background-color: #BFA76F;
            color: white;
            text-align: center;
        }
        .styled-table th, .styled-table td {
            padding: 10px 12px;
            border-bottom: 1px solid #DDDDDD;
            text-align: center;
            color: #4A4A4A;
        }
        .styled-table tbody tr:nth-of-type(even) {
            background-color: #F9F9F9;
        }
        .styled-table tbody tr:hover {
            background-color: #EFEFEF;
        }
    </style>
    """, unsafe_allow_html=True)
    st.markdown(f"<div class='styled-table-wrapper'>{styled_table}</div>", unsafe_allow_html=True)

# 📋 عرض الجدول
with col1:
    place_avg_rating = filtered.groupby(
        ['Region', 'City', 'Place Type', 'Place Name']
    )['Rating'].mean().reset_index()
    place_avg_rating['Rating'] = place_avg_rating['Rating'].round(2)
    render_styled_table(
        place_avg_rating[['Region', 'City', 'Place Type', 'Place Name',  'Rating']]
    )

# 📈 عرض الرسم الدائري بتنسيق احترافي
with col2:
    if not filtered.empty:
        sentiment_counts = filtered["Sentiment Label"].value_counts()
        total = sentiment_counts.sum()

        # إعداد البيانات
        sentiment_labels = ["positive", "neutral", "negative"]
        sizes = [sentiment_counts.get(label, 0) for label in sentiment_labels]
        percentages = [round((value / total) * 100, 1) if total > 0 else 0 for value in sizes]
        colors = {
            "positive": "#A3C9A8",
            "neutral": "#D9D9D9",
            "negative": "#D16666"
        }

        fig, ax = plt.subplots(figsize=(4.5, 4.5), dpi=100)
        ax.pie(
            sizes,
            startangle=140,
            colors=[colors[label] for label in sentiment_labels],
        )
        ax.axis('equal')
        ax.set_title("Sentiment Distribution", fontsize=12, color="black")
        ax.set_facecolor('#e6ebe0')
        fig.patch.set_facecolor('#e6ebe0')

        st.markdown("<div style='margin-top: 80px;'>", unsafe_allow_html=True)
        st.pyplot(fig)
        st.markdown("</div>", unsafe_allow_html=True)

        # 💬 بوكس التعريف
        st.markdown("""
<div style='margin-top: -20px; margin-left: 60px; font-size: 13px; line-height: 1.6; text-align: left;'>
    <b style='color: black;'>Legend</b><br>
    <span style='color:#A3C9A8;'>🟢 Positive: {:.1f}%</span><br>
    <span style='color:#A8A8A8;'>⚪ Neutral: {:.1f}%</span><br>
    <span style='color:#D16666;'>🔴 Negative: {:.1f}%</span>
</div>
""".format(*percentages), unsafe_allow_html=True)




    else:
        st.info("No data available for selected filters.")
