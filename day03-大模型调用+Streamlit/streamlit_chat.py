import os
import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="AI 对话", page_icon="💬")
st.title("💬 DeepSeek 对话")

client = OpenAI(
    api_key=***"DEEPSEEK_API_KEY", "***"),
    base_url="https://api.deepseek.com"
)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "你是一个有用的助手"}
    ]

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

if prompt := st.chat_input("说点什么："):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="deepseek-v4-pro",
            messages=st.session_state.messages,
            stream=False
        )
        reply = response.choices[0].message.content
        st.write(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})