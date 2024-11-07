import streamlit as st
import requests

# Title and Clear Chat button in the sidebar
st.sidebar.title("Facebook Review Sentiment Analyzer")
if st.sidebar.button("New Chat"):
    st.session_state["messages"] = []

st.header("How can I help?")

API_URL = "http://fastapi_service:8000/analyze/"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat history in a chat-like interface
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Get user input and send it to FastAPI
if prompt := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Send request to backend
    response = requests.post(
        API_URL,
        json={"messages": st.session_state.messages}
    )
    
    if response.status_code == 200:
        msg = response.json()["message"]
        st.session_state.messages.append({"role": "assistant", "content": msg})
        with st.chat_message("assistant"):
            st.write(msg)
    else:
        st.error("Error: Could not get a response from the server.")
