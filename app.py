import os, requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# ---------------- Config ----------------
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL   = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.1-8b-instruct")

st.set_page_config(page_title="Jason's Chatbot", page_icon="💬")
st.title("Jason's Testing Chatbot (OpenRouter)")

# ---------------- Helpers ----------------
def gen_openrouter(messages):
    if not OPENROUTER_API_KEY:
        raise RuntimeError(
            "Missing OPENROUTER_API_KEY. Set it in a .env file or Streamlit Secrets."
        )

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        # The two headers below are optional but recommended by OpenRouter:
        "HTTP-Referer": "https://example.com",     # change to your site if you want
        "X-Title": "Jason Testing Chatbot",
        "Content-Type": "application/json",
    }
    payload = {
        "model": OPENROUTER_MODEL,
        "messages": messages,   # OpenRouter supports the OpenAI-style chat format
        "temperature": 0.2,     # fixed; users can't change it
    }

    r = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=120,
    )
    r.raise_for_status()
    data = r.json()
    return data["choices"][0]["message"]["content"]

# ---------------- Chat state ----------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are a concise, helpful assistant. Keep in mind that the user's name is Jason Nguyen. Also keep it professional."
        },
        {
            "role": "assistant",
            "content": "Hi Jason! I currently work! Ask me anything (I’m running via OpenRouter)."
        },
    ]

# Render history (skip system)
for m in st.session_state.messages:
    if m["role"] == "system":
        continue
    with st.chat_message(m["role"]):
        st.write(m["content"])

# ---------------- Input & response ----------------
user_msg = st.chat_input("Type your message…")
if user_msg:
    st.session_state.messages.append({"role": "user", "content": user_msg})
    with st.chat_message("user"):
        st.write(user_msg)

    with st.chat_message("assistant"):
        try:
            # keep prompts small
            window = st.session_state.messages[-20:]
            answer = gen_openrouter(window)
            st.write(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error(str(e))
