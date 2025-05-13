import streamlit as st
import base64


# Helper to convert image to base64
def image_to_base64(path):
    with open(path, "rb") as image:
        return base64.b64encode(image.read()).decode()



# 🌿 تنسيقات الصفحة + الشريط الجانبي
st.markdown("""
<style>

html, body, .stApp {
    padding-top: 0px !important;
    margin-top: -70px !important;
}
main[data-testid="stAppViewContainer"] {
    padding-top: 0rem !important;
    margin-top: -70px !important;
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
/* خلفية الصفحة الرئيسية */
.stApp {
    background-color: #e6ebe0;
    color: black;
}
header, .css-18e3th9 {
    background-color: #e6ebe0 !important;
}
h1 {
    color: black !important;
    font-size: 36px;
}
video {
    border-radius: 12px;
    box-shadow: 0 0 10px rgba(0,0,0,0.2);
    margin-bottom: 30px;
}
</style>
""", unsafe_allow_html=True)


# 🖼️ Load all logos
tourism_logo = image_to_base64("pages/tourism_logo_clean.png")
sda_base64 = image_to_base64("SDA.png")
le_base64 = image_to_base64("le.png")

# ✅ Inject all logos in one row at the top-right
st.markdown(f"""
    <div style='display: flex; justify-content: flex-end; align-items: center; margin-top: 25px; margin-bottom: -10px; padding-right: 20px; gap: 15px;'>
        <img src="data:image/png;base64,{tourism_logo}" style="height: 60px;" alt="Tourism Authority Logo">
        <img src="data:image/png;base64,{sda_base64}" style="height: 40px;" alt="SDA Logo">
        <img src="data:image/png;base64,{le_base64}" style="height: 40px;" alt="Le Wagon Logo">
    </div>
""", unsafe_allow_html=True)



# 🏷️ عنوان الصفحة
st.markdown("<h1 style='text-align: center;'>Saudi Tourism Review Analysis</h1>", unsafe_allow_html=True)

# 🎥 تشغيل الفيديو المحلي بدون تحكمات
video_path = "video.mp4"
with open(video_path, "rb") as video_file:
    video_bytes = video_file.read()
    encoded_video = base64.b64encode(video_bytes).decode()

video_html = f"""
<video autoplay muted loop playsinline style="width: 100%; height: auto; border-radius: 12px; box-shadow: 0 0 10px rgba(0,0,0,0.2);">
    <source src="data:video/mp4;base64,{encoded_video}" type="video/mp4">
    Your browser does not support the video tag.
</video>
"""
st.markdown(video_html, unsafe_allow_html=True)

# 📝 محتوى الصفحة (المقدمة)
st.markdown("""
### Vision 2030 & Tourism Growth

As part of **Saudi Arabia’s Vision 2030**, the Kingdom set an ambitious goal:
> **- To welcome 100 million tourists annually by the year 2030.**

This milestone was already achieved in **2023**, with over **100.9 million** visitors — a significant national accomplishment.

---

### 💡 Project Motivation

Inspired by this success, our project was designed to explore:
- How satisfied are tourists with their experiences in Saudi Arabia?
- What are the common strengths and weaknesses in tourist services?
- Are there differences in sentiment between regions or types of attractions?

---

### Data

To answer these questions, we:
- Collected a sample of **real tourist reviews** using the **Google Places API**
- Focused on reviews from different types of places (hotels, restaurants, parks, etc.)
- Applied **Natural Language Processing (NLP)** techniques to analyze the **sentiment** behind the reviews

---
""")

# 👥 قسم الفريق في الشريط الجانبي
st.sidebar.markdown(
    """
    <div style='padding-top: 20px;'>
        <h2 style='text-align: left; font-size: 22px; color: black;'>Team Members</h2>
        <ul style='list-style-type: none; padding: 0; font-size: 14px; color: black;'>
            <li style='margin-bottom: 15px;'>
                <img src='https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png' style='width:16px; vertical-align:middle; margin-right:5px;'>
                <a href='https://github.com/HayaAlsubie' target='_blank' style='text-decoration: none; color: #00BFFF;'>Haya Alsubie</a><br>
                <a href='https://linkedin.com/in/haya-ajab' target='_blank' style='font-size: 12px; color: #AAAAAA;'>LinkedIn Profile</a>
            </li>
            <li style='margin-bottom: 15px;'>
                <img src='https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png' style='width:16px; vertical-align:middle; margin-right:5px;'>
                <a href='https://github.com/SarahxHM' target='_blank' style='text-decoration: none; color: #00BFFF;'>Sarah Alshehri</a><br>
                <a href='https://linkedin.com/in/sarah-alshehri-mis/' target='_blank' style='font-size: 12px; color: #AAAAAA;'>LinkedIn Profile</a>
            </li>
            <li style='margin-bottom: 15px;'>
                <img src='https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png' style='width:16px; vertical-align:middle; margin-right:5px;'>
                <a href='https://github.com/farajay96' target='_blank' style='text-decoration: none; color: #00BFFF;'>Ali Alfaraj</a><br>
                <a href='https://linkedin.com/in/ali-y-alfaraj-367628163' target='_blank' style='font-size: 12px; color: #AAAAAA;'>LinkedIn Profile</a>
            </li>
            <li style='margin-bottom: 15px;'>
                <img src='https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png' style='width:16px; vertical-align:middle; margin-right:5px;'>
                <a href='https://github.com/xshmbr' target='_blank' style='text-decoration: none; color: #00BFFF;'>Shumoukh</a><br>
                <a href='https://linkedin.com/in/shoumkh-albarraq' target='_blank' style='font-size: 12px; color: #AAAAAA;'>LinkedIn Profile</a>
            </li>
            <li style='margin-bottom: 15px;'>
                <img src='https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png' style='width:16px; vertical-align:middle; margin-right:5px;'>
                <a href='https://github.com/khawlah57' target='_blank' style='text-decoration: none; color: #00BFFF;'>Khawlah Aldarwish</a><br>
                <a href='https://linkedin.com/in/khawlah' target='_blank' style='font-size: 12px; color: #AAAAAA;'>LinkedIn Profile</a>
            </li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True
)


# 🔃 Helper to convert image to base64
def image_to_base64(path):
    with open(path, "rb") as image:
        return base64.b64encode(image.read()).decode()
