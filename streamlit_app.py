import streamlit as st
from openai import OpenAI

# =============================
# CONFIGURATION
# =============================
st.set_page_config(page_title="FinLitAI Tutor NG 🇳🇬", page_icon="💰")

st.title("FinLitAI Tutor NG 🇳🇬")
st.write("Your AI money tutor (Pidgin + English). Learn, avoid scams, and grow your money!")

# =============================
# LOAD OPENAI API KEY
# =============================
api_key = st.secrets.get("OPENAI_API_KEY")

if not api_key:
    st.warning("⚠️ OpenAI API key not found. Enter it below for testing.")
    api_key = st.text_input("Enter OpenAI API Key", type="password")

if not api_key:
    st.stop()

client = OpenAI(api_key=api_key)

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
lesson = st.sidebar.selectbox("Choose a topic", ["Savings", "Budgeting", "Scams", "Banking Basics"])

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
options = ["Save ₦1000 every week", "Invest ₦5k get ₦50k in 2 days", "Open bank account", "Track your expenses"]
answer = st.sidebar.radio(quiz_question, options)

if st.sidebar.button("Submit Answer"):
    if answer == "Invest ₦5k get ₦50k in 2 days":
        st.sidebar.success("Correct! 🎉")
        st.session_state.score += 1
    else:
        st.sidebar.error("Wrong! Try again.")

st.sidebar.write(f"Score: {st.session_state.score}")

# =============================
# CHAT INTERFACE
# =============================
st.subheader("💬 Ask FinLitAI")
for msg in st.session_state.messages:
    with st.chat_message(msg['role']):
        st.markdown(msg['content'])

user_input = st.chat_input("Ask about money in Pidgin or English...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # SYSTEM PROMPT
    system_prompt = """
You are FinLitAI Tutor NG.
Teach financial literacy in simple English and Nigerian Pidgin.
Use relatable Nigerian examples (Ajo, POS, betting, scams).
Be friendly, clear, and short.
If message looks like scam, warn user clearly.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": system_prompt}, *st.session_state.messages]
        )
        reply = response.choices[0].message.content
    except Exception as e:
        reply = "⚠️ Error connecting to AI. Check your API key or internet connection."
        st.error(str(e))

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)

# =============================
# FOOTER
# =============================
st.markdown("---")
st.markdown("🚀 Built with ❤️ for Nigerian youth | FinLitAI Tutor NG")
