import streamlit as st

# =============================
# APP CONFIG
# =============================
st.set_page_config(page_title="FinLitAI Tutor NG 🇳🇬", page_icon="💰")
st.title("FinLitAI Tutor NG 🇳🇬")
st.success("🇳🇬 Learn money the smart way. Avoid scams. Build wealth.")
st.info("💡 Try: 'How I fit save money?' or 'Is this investment legit?'")

# =============================
# SESSION STATE
# =============================
if "messages" not in st.session_state:
    st.session_state.messages = []
if "score" not in st.session_state:
    st.session_state.score = 0

# =============================
# LESSONS SIDEBAR
# =============================
st.sidebar.header("📚 Lessons")
lesson = st.sidebar.selectbox(
    "Choose a topic",
    ["Savings", "Budgeting", "Scams", "Banking Basics"]
)

LESSONS = {
    "Savings": "Savings na when you keep part of your money for future use instead of spending everything.",
    "Budgeting": "Budget na plan wey show how you go spend your money so you no go finish am.",
    "Scams": "Scam na trick wey people use collect your money. If e too good to be true, na scam.",
    "Banking Basics": "Bank na place wey you fit keep money safe and send money to others."
}

if st.sidebar.button("Show Lesson"):
    st.sidebar.success(LESSONS[lesson])

# =============================
# QUIZ SIDEBAR
# =============================
st.sidebar.header("🧠 Quick Quiz")
quiz_question = "Which one be scam?"
options = [
    "Save ₦1000 every week",
    "Invest ₦5k get ₦50k in 2 days",
    "Open bank account",
    "Track your expenses"
]
answer = st.sidebar.radio(quiz_question, options)

if st.sidebar.button("Submit Answer"):
    if answer == "Invest ₦5k get ₦50k in 2 days":
        st.sidebar.success("Correct! 🎉")
        st.session_state.score += 1
    else:
        st.sidebar.error("Wrong! Try again.")

st.sidebar.write(f"Score: {st.session_state.score}")

# =============================
# BACKUP CHAT FUNCTION
# =============================
def backup_response(user_input):
    text = user_input.lower()
    if "save" in text:
        return "💡 Start small. Keep part of your money weekly. Even ₦500 helps. Avoid unnecessary spending."
    elif "budget" in text:
        return "📊 Budget means planning your money: divide your money into needs, wants, and savings."
    elif "scam" in text or "invest" in text:
        return "⚠️ This looks like a scam. High returns in 2 days are risky. Always verify before investing."
    elif "bank" in text:
        return "🏦 Banks keep your money safe and help you send/receive money securely."
    else:
        return "🤖 I'm here to help you learn money basics. Ask about savings, scams, or budgeting!"

# =============================
# CHAT INTERFACE
# =============================
st.subheader("💬 Ask FinLitAI")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask about money in Pidgin or English...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Use backup mode only (offline safe)
    reply = backup_response(user_input)
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)
    st.info("⚠️ Running in demo backup mode (offline responses).")

# =============================
# FOOTER WITH 3MTT BRANDING
# =============================
st.markdown(
    """
    <hr style="border-top: 1px solid #ddd;">
    <div style="text-align: center; padding: 20px 0; color: #666; font-size: 14px;">
        <img src="https://raw.githubusercontent.com/YOUR_GITHUB_USERNAME/finlitai-tutor-ng/main/3mtt-nextgen-logo.png" 
             alt="3MTT NextGen Logo" 
             style="height: 60px; margin-bottom: 10px;">
        <br>
        Built with love for the <strong>3MTT NextGen Knowledge Showcase</strong> 🇳🇬<br>
        Powered by AI • Individual Submission • Education Pillar
    </div>
    """,
    unsafe_allow_html=True
)
