import streamlit as st
from openai import OpenAI

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
# BACKUP RESPONSE FUNCTION
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

    # Hybrid AI: Live if API key exists, else fallback
    try:
        api_key = st.secrets.get("OPENAI_API_KEY")
        if not api_key:
            raise Exception("No API key found")

        client = OpenAI(api_key=api_key)
        system_prompt = """
You are FinLitAI Tutor NG.

Teach financial literacy in simple English and Nigerian Pidgin.

IMPORTANT:
- If user message looks like a scam, clearly warn them.
- Explain WHY it is a scam.
- Suggest a safer alternative.

Use Nigerian examples (Ajo, POS, betting, Ponzi schemes).
Be friendly, clear, and short.
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": system_prompt}, *st.session_state.messages]
        )
        reply = response.choices[0].message.content

    except Exception:
        reply = backup_response(user_input)
        st.info("⚠️ Running in demo backup mode (offline responses).")

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)

# =============================
# GREEN 3MTT-THEMED FOOTER
# =============================
st.markdown(
    """
    <hr style="border-top:2px solid #228B22; margin:40px 0 20px;">
    <div style="text-align:center; background-color:#004d00; color:#f0f8ff; font-size:14px; padding:20px 10px; border-radius:8px; margin:0 auto; max-width:800px;">
        Fellow ID: <strong>FE/26/4246539238</strong><br>
        Submitted by <strong>Adama Nuhu</strong><br>
        <span style="color:#32CD32; font-weight:bold;">3MTT NextGen Knowledge Showcase</span> 🇳🇬<br>
        Education Pillar • Powered by AI
    </div>
    """,
    unsafe_allow_html=True
)
