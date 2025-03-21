"""
TalentScout Hiring Assistant
-----------------------------
A Streamlit application that serves as an intelligent hiring assistant for
initial candidate screening, gathering information, and posing technical questions.
"""
import streamlit as st
import os
from dotenv import load_dotenv
from chat_manager import ChatManager
from utils import sanitize_input, format_candidate_info

# Load environment variables
load_dotenv()

def initialize_session_state():
    """Initialize session state variables if they don't exist."""
    if 'chat_manager' not in st.session_state:
        # Get API key from environment or Streamlit secrets
        api_key = os.getenv("GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY", None)

        if not api_key:
            st.error("Google API key not found. Please set it in your environment or Streamlit secrets.")
            st.stop()

        st.session_state.chat_manager = ChatManager(api_key=api_key)

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    if 'candidate_info' not in st.session_state:
        st.session_state.candidate_info = {}

def main():
    """Main function to run the Streamlit application."""
    st.set_page_config(
        page_title="TalentScout Hiring Assistant",
        page_icon="🤖",
        layout="wide"
    )

    initialize_session_state()

    # Application title and description
    st.title("TalentScout Hiring Assistant")
    st.markdown("""
    Welcome to the TalentScout Hiring Assistant! This AI-powered chatbot will guide you through
    the initial screening process for technology positions at our company.
    
    The assistant will ask you about your background, experience, and technical skills,
    and then pose relevant technical questions based on your declared tech stack.
    """)

    # Sidebar for displaying candidate information
    st.sidebar.title("Candidate Information")
    if st.session_state.chat_manager.candidate_info:
        st.sidebar.markdown(format_candidate_info(st.session_state.chat_manager.candidate_info))
    else:
        st.sidebar.markdown("No information collected yet.")

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Handle initial greeting if no messages yet
    if not st.session_state.messages:
        # Initial greeting from the assistant
        chat_manager = st.session_state.chat_manager
        greeting = chat_manager.process_message("Hello")

        # Add assistant message to the session state
        st.session_state.messages.append({"role": "assistant", "content": greeting})

        # Force a rerun to display the greeting
        st.rerun()

    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Sanitize input
        safe_prompt = sanitize_input(prompt)

        # Add user message to session state
        st.session_state.messages.append({"role": "user", "content": safe_prompt})

        # Display user message
        with st.chat_message("user"):
            st.markdown(safe_prompt)

        # Generate and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                chat_manager = st.session_state.chat_manager
                response = chat_manager.process_message(safe_prompt)
                st.markdown(response)

        # Add assistant message to session state
        st.session_state.messages.append({"role": "assistant", "content": response})

        # Update sidebar with latest candidate info
        st.sidebar.empty()
        st.sidebar.title("Candidate Information")
        st.sidebar.markdown(format_candidate_info(chat_manager.candidate_info))

        # Check if conversation has ended
        if chat_manager.conversation_stage == "end":
            st.success("Initial screening complete! Thank you for your time.")

if __name__ == "__main__":
    main()