import streamlit as st
import pandas as pd
import requests
import os

OLLAMA_API_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "gemma3"  # You can change this to your preferred local model

BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="Local AI Chatbot with CSV", layout="wide")
st.title("📊 Local AI Chatbot (Ollama) with CSV Upload")

# Reset Database Button
if st.button("Reset Database 🗑️"):
    try:
        resp = requests.post(f"{BACKEND_URL}/reset_db/")
        if resp.status_code == 200:
            st.success("Database reset successfully!")
        else:
            st.error(f"Failed to reset database: {resp.text}")
    except Exception as e:
        st.error(f"Error: {e}")

# File uploader for CSV
data = None
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
if uploaded_file:
    data = pd.read_csv(uploaded_file)
    st.write("### Preview of uploaded CSV:")
    st.dataframe(data.head())

# Chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

st.write("---")
st.write("### Chat with your CSV using Ollama")

user_input = st.text_input("You:", key="user_input")

if st.button("Send") and user_input:
    # Prepare context from CSV (first 5 rows as string, for simplicity)
    csv_context = ""
    if data is not None:
        csv_context = data.head().to_csv(index=False)
    else:
        csv_context = "No CSV uploaded."

    # Compose prompt
    prompt = f"You are a helpful data assistant. Here is some CSV data:\n{csv_context}\nUser question: {user_input}"

    # Call Ollama API
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        ai_response = result.get("response", "[No response from model]")
    except Exception as e:
        ai_response = f"Error: {e}"

    # Update chat history
    st.session_state["messages"].append((user_input, ai_response))

# Display chat history
for user_msg, ai_msg in st.session_state["messages"]:
    st.markdown(f"**You:** {user_msg}")
    st.markdown(f"**AI:** {ai_msg}")
    st.write("") 