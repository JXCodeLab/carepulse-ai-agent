import streamlit as st
from langchain_core.messages import HumanMessage
from agent import carepulse_app

st.set_page_config(
    page_title="CarePulse Health AI | Medical Portal",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End Clinical UI Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .stApp {
        background: radial-gradient(circle at top right, #0e2029 0%, #071015 100%);
        color: #e2e8f0;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0b151b !important;
        border-right: 1px solid #162732;
    }

    .sidebar-brand-card {
        background: #0f1c24;
        border: 1px solid #1a303d;
        border-radius: 14px;
        padding: 16px;
        margin-bottom: 16px;
    }

    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(16, 185, 129, 0.12);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.3px;
    }

    .pulse-dot {
        width: 7px;
        height: 7px;
        background-color: #10b981;
        border-radius: 50%;
        box-shadow: 0 0 10px #10b981;
    }

    .clinic-feature-item {
        display: flex;
        align-items: flex-start;
        gap: 10px;
        padding: 8px 0;
        border-bottom: 1px solid #15242e;
        font-size: 13px;
        color: #94a3b8;
    }
    
    .clinic-feature-item:last-child {
        border-bottom: none;
    }

    .feature-icon {
        font-size: 15px;
        margin-top: 2px;
    }

    .emergency-card {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.12) 0%, rgba(15, 28, 36, 0.8) 100%);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 12px;
        padding: 12px 14px;
        margin-top: 14px;
    }

    /* Main Header Hero */
    .hero-container {
        display: flex;
        align-items: center;
        gap: 22px;
        background: linear-gradient(90deg, #0e232b 0%, #0a161c 100%);
        border: 1px solid #1e3947;
        border-radius: 18px;
        padding: 20px 24px;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
    }

    .hero-img {
        width: 90px;
        height: 90px;
        border-radius: 14px;
        object-fit: cover;
        border: 2px solid #2a4d60;
    }

    .hero-text h1 {
        margin: 0;
        font-size: 24px;
        font-weight: 700;
        color: #f8fafc;
        letter-spacing: -0.5px;
    }

    .hero-text p {
        margin: 6px 0 0 0;
        color: #38bdf8;
        font-size: 13px;
    }

    /* Chat Messages Look & Feel */
    .stChatMessage {
        border-radius: 16px !important;
        padding: 12px 18px !important;
        margin-bottom: 12px !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }

    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarUser"]) {
        background: #0f2c27 !important;
        border: 1px solid #1b5349 !important;
    }

    div[data-testid="stChatMessage"]:has(div[data-testid="stChatMessageAvatarAssistant"]) {
        background: #0d1b22 !important;
        border: 1px solid #1a3342 !important;
    }

    .stChatInputContainer {
        border-radius: 14px !important;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.image(
        "https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?auto=format&fit=crop&w=800&q=80",
        caption="CarePulse Specialized Care Center",
        use_container_width=True
    )

    st.markdown("""
    <div class="sidebar-brand-card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <span style="font-weight: 700; color: #f1f5f9; font-size: 15px;">Reception Desk</span>
            <span class="status-pill"><span class="pulse-dot"></span> LIVE</span>
        </div>
        <p style="font-size: 12px; color: #94a3b8; margin: 0;">Sara is active to assist with doctor schedules, consultations, and appointments.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### 🏥 Facility Information")
    st.markdown("""
    <div class="clinic-feature-item">
        <span class="feature-icon">📍</span>
        <div><b>Location</b><br>Executive Health Wing, CarePulse Plaza</div>
    </div>
    <div class="clinic-feature-item">
        <span class="feature-icon">⏰</span>
        <div><b>OPD Hours</b><br>09:00 AM – 09:00 PM (Mon – Sat)</div>
    </div>
    <div class="clinic-feature-item">
        <span class="feature-icon">🛡️</span>
        <div><b>Accreditation</b><br>ISO 9001 Certified Clinical Center</div>
    </div>
    <div class="clinic-feature-item">
        <span class="feature-icon">🧪</span>
        <div><b>Services</b><br>Cardiology, Dermatology, Orthopedics, General OPD</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="emergency-card">
        <div style="color: #f87171; font-weight: 700; font-size: 12px; letter-spacing: 0.5px;">🚨 24/7 MEDICAL EMERGENCY</div>
        <div style="font-size: 14px; font-weight: 600; color: #fca5a5; margin-top: 4px;">UAN: +92 (51) 111-227-378</div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    if st.button("🧹 Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# ----------------- MAIN UI -----------------
st.markdown("""
<div class="hero-container">
    <img src="https://images.unsplash.com/photo-1629909613654-28e377c37b09?auto=format&fit=crop&w=250&q=80" class="hero-img" alt="Hospital Reception" />
    <div class="hero-text">
        <h1>CarePulse Medical Center</h1>
        <p>Verified AI Receptionist • Real-time Consultations & Instant Slot Reservations</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Message state initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display conversation
for msg in st.session_state.messages:
    role = "user" if msg.type == "human" else "assistant"
    with st.chat_message(role):
        st.markdown(msg.content)

# Input Box
prompt = st.chat_input("Poochiye: Doctors list, timings, ya appointment booking...")
if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append(HumanMessage(content=prompt))

    with st.chat_message("assistant"):
        with st.spinner("Connecting with Sara..."):
            try:
                result = carepulse_app.invoke({"messages": st.session_state.messages})
                reply = result["messages"][-1].content
                st.markdown(reply)
                st.session_state.messages.append(result["messages"][-1])
            except Exception as e:
                st.error(f"Error: {e}")