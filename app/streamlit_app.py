import streamlit as st
from service import ChatService
from repository import OpenAIRepository, DDGSearchRepository
import os

# App title and description
st.title("🤖 AI Chat Assistant")
st.markdown("""
This assistant uses OpenAI's API to answer your questions.  
Please enter your OpenAI API key to begin.
""")

if 'service' not in st.session_state:
    st.session_state.service = None
    st.session_state.api_key = ""

with st.sidebar:
    st.header("🔑 OpenAI Configuration")
    api_key = st.text_input(
        "Enter your OpenAI API key",
        type="password",
        value=st.session_state.api_key
    )
    
    if st.button("Save API Key"):
        if not api_key.startswith('sk-'):
            st.error("Please enter a valid OpenAI API key")
        else:
            os.environ["OPENAI_API_KEY"] = api_key
            st.session_state.service = ChatService(
                OpenAIRepository(),
                DDGSearchRepository()
            )
            st.session_state.api_key = api_key
            st.success("API key saved successfully!")

if st.session_state.service:
    st.subheader("💬 Chat")
    user_input = st.text_input("Ask me anything:")
    search_toggle = st.checkbox("Include web search results", value=True)
    
    if user_input:
        with st.spinner("Generating response..."):
            response = st.session_state.service.ask_question(
                user_input,
                perform_search=search_toggle
            )
        st.text_area("Response:", value=response, height=200)
else:
    st.warning("Please enter your OpenAI API key in the sidebar to begin")