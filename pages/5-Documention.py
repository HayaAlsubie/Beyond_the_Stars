import streamlit as st
from Introduction import image_to_base64

# ─────────────────────────────
# PAGE CONFIG & STYLING
# ─────────────────────────────
st.set_page_config(page_title="Summary ", layout="wide")

# Custom CSS styling (matches other pages)
st.markdown("""
<style>
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


# ─────────────────────────────
# RECOMMENDATIONS SECTION
# ─────────────────────────────
st.markdown("""
<h2 style='margin-top: 50px;'> Recommendations</h2>
<ul style='font-size: 17px; line-height: 1.8;'>
    <li>Focus improvement efforts on cities with high negative sentiment and low ratings.</li>
    <li>Standardize service quality across hospitality providers, especially in southern and northern cities.</li>
    <li>Promote highly-rated experiences in international tourism campaigns.</li>
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
sda_base64 = image_to_base64("SDA.png")
le_base64 = image_to_base64("le.png")

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
