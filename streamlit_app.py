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

# Initialize OpenAI Client (Make sure to set your API key in Streamlit Secrets)
client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY", "your-key-here"))

st.title("💰 FinLitAI Tutor NG 🇳🇬")
st.markdown("### Smart Money Assistant for Nigerians 🇳🇬")
st.success("Learn • Save • Avoid Scams")

# =============================
# SESSION STATE
# =============================
if "messages" not in st.session_state:
    # System message sets the "personality" of the bot
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful Nigerian financial literacy tutor. You explain concepts like inflation, budgeting, and investment in a way that relates to the Nigerian economy. Use local context (Naira, Treasury Bills, savings apps, Ajo). Warn users against Ponzis and 'get rich quick' schemes."}
    ]

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

if "daily_tip" not in st.session_state:
    st.session_state.daily_tip = random.choice(tips)

st.info(f"💡 Tip of the Day: {st.session_state.daily_tip}")

# =============================
# SIDEBAR TOOLS
# =============================
st.sidebar.title("📊 Financial Tools")
st.sidebar.markdown("---")

# Quick Savings Calculator
st.sidebar.subheader("Naira Savings Goal 🇳🇬")
goal_amount = st.sidebar.number_input("Target Amount (₦)", min_value=0, value=100000)
monthly_save = st.sidebar.number_input("Monthly Savings (₦)", min_value=1, value=5000)

if monthly_save > 0:
    months = goal_amount / monthly_save
    st.sidebar.write(f"It will take you **{months:.1f} months** to hit your goal!")

st.sidebar.markdown("---")
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = [st.session_state.messages[0]] # Keep the system prompt
    st.rerun()

# =============================
# CHAT INTERFACE
# =============================
# Display chat history (skipping the hidden system message)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Chat input logic
if prompt := st.chat_input("How can I help you manage your money today?"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response from OpenAI
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo", # or "gpt-4"
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    
    # Save assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": response})
