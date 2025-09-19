import os, streamlit as st
from openai import OpenAI

st.set_page_config(page_title="My Chatbot", page_icon="💬")
st.title("💬 My Chatbot")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

if "history" not in st.session_state:
    st.session_state.history = []

q = st.chat_input("Ask me anything…")
if q:
    st.session_state.history.append(("user", q))
    with st.chat_message("user"): st.write(q)
    with st.chat_message("assistant"):
        r = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role":"system","content":"Be concise and helpful."},
                      {"role":"user","content": q}]
        )
        a = r.choices[0].message.content
        st.write(a)
        st.session_state.history.append(("assistant", a))

for role, msg in st.session_state.history:
    with st.chat_message(role): st.write(msg)
