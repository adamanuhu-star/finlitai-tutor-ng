import streamlit as st
from openai import OpenAI
import random

# =============================
# APP CONFIG
# =============================
st.set_page_config(
    page_title="FinLitAI Tutor NG 🇳🇬",
    page_icon="💰",
    layout="centered"
)

st.title("💰 FinLitAI Tutor NG 🇳🇬")
st.markdown("### Smart Money Assistant for Nigerians 🇳🇬")
st.success("Learn • Save • Avoid Scams")

# =============================
# SESSION STATE
# =============================
if "messages" not in st.session_state:
    st.session_state.messages = []

# =============================
# DAILY TIP
# =============================
tips = [
    "Save at least 10% of your income.",
    "Avoid 'get rich quick' investments.",
    "Track your expenses weekly.",
    "Use Ajo or bank savings wisely.",
    "Never share your OTP or ATM PIN.",
    "If it sounds too good, it's likely a scam.",
]

st.info(f"💡 Tip of the Day: {random.choice(tips)}")

# =============================
# SIDEBAR TOOLS
# =============================
st.sidebar.title("📊
