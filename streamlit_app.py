# Chat interface with fallback
st.subheader("💬 Ask FinLitAI")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask about money in Pidgin or English...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Backup AI responses
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

    # Try real API if you want (optional)
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "You are FinLitAI Tutor NG teaching financial literacy."}, 
                      *st.session_state.messages]
        )
        reply = response.choices[0].message.content
    except Exception:
        reply = backup_response(user_input)
        st.info("⚠️ Running in demo backup mode (offline responses).")

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)
