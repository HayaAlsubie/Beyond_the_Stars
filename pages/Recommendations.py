import streamlit as st
from introduction import image_to_base64

# ─────────────────────────────
# PAGE CONFIG & STYLING
# ─────────────────────────────
st.set_page_config(page_title="Summary ", layout="wide")


# Custom CSS styling (matches other pages)
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

/* Page background */
.stApp {
    background-color: #e6ebe0;
    color: black;
}




/* Header bar */
header[data-testid="stHeader"] {
    background-color: #e6ebe0 !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #153f2e !important;
}
section[data-testid="stSidebar"] * {
    color: #e6ebe0 !important;
}

/* Highlight current page */
[data-testid="stSidebarNav"] ul li a[aria-current="page"] {
    color: #CBA135 !important;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)




tourism_logo = image_to_base64("pages/tourism_logo_clean.png")
st.markdown(f"""
<div style='text-align: right; margin-top: 25px; margin-bottom: -10px; padding-right: 20px;'>
    <img src="data:image/png;base64,{tourism_logo}" style="height: 60px;" alt="Tourism Authority Logo">
</div>
""", unsafe_allow_html=True)







# ─────────────────────────────
# RECOMMENDATIONS SECTION
# ─────────────────────────────
st.markdown("""
<h2 style='margin-top: 10px;'>Recommendations</h2>
<ul style='font-size: 17px; line-height: 1.8;'>
    <li>Launch targeted training programs for hospitality staff in cities with frequent complaints about service quality.</li>
    <li>Promote highly-rated locations like Riyadh and Al Khobar as tourism success models and use their strengths to guide improvements elsewhere.</li>
    <li>Provide multilingual support in tourist-facing services, as negative reviews in English often reflect unmet communication needs.</li>
    <li>Recognize and reward high-performing venues with visibility in official tourism platforms as a motivation for others.</li>
</ul>
""", unsafe_allow_html=True)

# ─────────────────────────────
# CONCLUSION SECTION
# ─────────────────────────────
st.markdown("""
<!-- Inspirational closing message -->
<div style='font-size: 17px; margin-top: 30px; text-align: center;'>
Saudi Arabia is well on its way to becoming a top global tourist destination.<br>
By listening to our visitors, we can shape a world-class tourism experience that reflects the Kingdom’s culture and hospitality.
</div>
""", unsafe_allow_html=True)




# 🖼️ Load logos
sda_base64 = image_to_base64("pages/SDA.png")
le_base64 = image_to_base64("pages/le.png")

# ✅ Inject logos at bottom right of introduction page
st.markdown(f"""
    <style>
        .bottom-logos {{
            display: flex;
            justify-content: flex-end;
            align-items: center;
            margin-top: 30px;
            margin-right: 40px;
        }}
        .bottom-logos img {{
            height: 35px;
            margin-left: 10px;
        }}
    </style>

    <div class="bottom-logos">
        <img src="data:image/png;base64,{sda_base64}" alt="SDA Logo">
        <img src="data:image/png;base64,{le_base64}" alt="LeWagon Logo">
    </div>
""", unsafe_allow_html=True)
