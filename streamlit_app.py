import streamlit as st
from openai import OpenAI

# =============================
# CONFIGURATION
# =============================
st.set_page_config(page_title="FinLitAI Tutor NG 🇳🇬", page_icon="💰")

st.title("FinLitAI Tutor NG 🇳🇬")
st.success("🇳🇬 Learn money the smart way. Avoid scams. Build wealth.")
st.write("Your AI money tutor (Pidgin + English).")

st.info("💡 Try: 'How I fit save money?' or 'Is this investment legit?'")

# =============================
# LOAD OPENAI API KEY
# =============================
api_key = st.text_input("Enter OpenAI API Key", type="password")

if not api_key:
    st.stop()

client = OpenAI(api_key=api_key)

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

    # SYSTEM PROMPT (UPGRADED FOR WINNING)
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

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                *st.session_state.messages
            ]
        )
        reply = response.choices[0].message.content

    except Exception as e:
        error_msg = str(e)

        if "401" in error_msg or "invalid_api_key" in error_msg:
            reply = "⚠️ Invalid API key. Please check your Streamlit secrets."
            st.warning("Invalid API key detected.")

        elif "quota" in error_msg or "billing" in error_msg:
            reply = "⚠️ API quota exceeded. Please check your billing."
            st.warning("Quota exceeded.")

        else:
            reply = "⚠️ Network or server issue. Please try again."
            st.warning("Temporary error.")

    st.session_state.messages.append({"role": "assistant", "content": reply})

    with st.chat_message("assistant"):
        st.markdown(reply)

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
