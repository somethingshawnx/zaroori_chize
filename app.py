import streamlit as st
import requests
import json
import time

# Configuration
API_URL = "http://localhost:8000/chat"

# Streamlit Page Setup
st.set_page_config(
    page_title="Multi-Agent Productivity Ecosystem",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Apply some custom CSS for a cleaner look
st.markdown("""
<style>
    .stChatFloatingInputContainer {
        padding-bottom: 2rem;
    }
    .user-greeting {
        font-size: 1.2rem;
        color: #555;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Application Header
st.title("🤖 Personal Productivity Ecosystem")
st.markdown("<p class='user-greeting'>Welcome to your local, free-tier multi-agent assistant powered by CrewAI and Groq.</p>", unsafe_allow_html=True)

# Sidebar with system info
with st.sidebar:
    st.header("System Status")
    
    # Check Backend Connection
    try:
        response = requests.get("http://localhost:8000/")
        if response.status_code == 200:
            st.success("Backend API: Connected (FastAPI)")
        else:
            st.error(f"Backend API: Error {response.status_code}")
    except requests.exceptions.ConnectionError:
        st.error("Backend API: Disconnected (Ensure main.py is running)")
        
    st.markdown("---")
    st.subheader("Active Agents")
    st.markdown("- **Task Manager Agent**: Prioritizes and structures work.")
    st.markdown("- **Research Analyst Agent**: Finds and summarizes information from the web.")
    
    st.markdown("---")
    st.subheader("Infrastructure")
    st.markdown("- **LLM**: Llama 3 (via Groq Free Tier)")
    st.markdown("- **Memory**: Pinecone Serverless (Free Tier)")
    st.markdown("- **Orchestration**: CrewAI")

# Session State for Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("How can the agents help you today? (e.g., 'Research Next.js caching and make a study plan')"):
    
    # 1. Add user message to state and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Call the Backend API
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # Show a spinner while the crew is working
        with st.spinner("The Crew is working on your request (this may take 10-20 seconds as multiple agents collaborate)..."):
            try:
                # Send request to FastAPI backend
                payload = {"message": prompt}
                response = requests.post(API_URL, json=payload, timeout=120)  # Long timeout for agent processing
                
                if response.status_code == 200:
                    result = response.json().get("response", "Error: No response generated.")
                    # Display the final result
                    message_placeholder.markdown(result)
                    # Add to history
                    st.session_state.messages.append({"role": "assistant", "content": result})
                else:
                    error_msg = f"API Error ({response.status_code}): {response.text}"
                    message_placeholder.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
                    
            except requests.exceptions.ConnectionError:
                error_msg = "Could not connect to the backend. Please ensure the FastAPI server (main.py) is running on port 8000."
                message_placeholder.error(error_msg)
            except requests.exceptions.Timeout:
                error_msg = "The request timed out. The agents took too long to respond."
                message_placeholder.error(error_msg)
            except Exception as e:
                error_msg = f"An unexpected error occurred: {str(e)}"
                message_placeholder.error(error_msg)
