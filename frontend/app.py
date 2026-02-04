import sys
import time
import streamlit as st
import requests
import json
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
import os

# Backend API base URL
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Set up the title and introduction for the app
st.set_page_config(page_title="Chat a lot.. knows nothing", layout="wide")
st.title("📚 Chat a lot.. knows nothing")
st.markdown("Upload your documents and ask questions about them!")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    
if "documents" not in st.session_state:
    st.session_state.documents = []

# Sidebar for document management
st.sidebar.header("📄 DOCUMENT MANAGEMENT")

# Display uploaded documents
def load_documents():
    """Fetch all uploaded documents from the backend"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/documents/")
        if response.status_code == 200:
            return response.json().get("documents", [])
    except Exception as e:
        st.sidebar.error(f"Failed to load documents: {str(e)}")
    return []

# Display current documents
documents = load_documents()
print(f"{documents}", file=sys.stderr)  
st.session_state.documents = documents

if documents:
    st.sidebar.subheader(f"Uploaded Documents ({len(documents)})")
    for doc in documents:
        col1, col2 = st.sidebar.columns([3, 1])
        with col1:
            st.caption(f"📄 {doc['file_name']}")
        with col2:
            if st.button("🗑️", key=f"delete_{doc['document_id']}"):
                # Delete document
                try:
                    response = requests.delete(
                        f"{BACKEND_URL}/api/documents/",
                        json={"document_id": doc['document_id']}
                    )
                    if response.status_code == 200:
                        st.sidebar.success("Document deleted!")
                        st.rerun()
                    else:
                        st.sidebar.error("Failed to delete document")
                except Exception as e:
                    st.sidebar.error(f"Error: {str(e)}")
else:
    st.sidebar.info("No documents uploaded yet. Upload one to get started!")

# File upload section
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = "uploader_initial"
    
st.sidebar.subheader("Upload New Document")
uploaded_file = st.sidebar.file_uploader(
    "Choose a file",
    type=["csv", "pdf", "docx", "doc", "png", "jpg", "jpeg"],
    label_visibility="collapsed",
    key=st.session_state.uploader_key
)

if uploaded_file:
    if st.sidebar.button("📤 Upload & Process", use_container_width=True):
        with st.sidebar.spinner("Processing document..."):
            try:
                # Upload file to backend
                files = {'file': (uploaded_file.name, uploaded_file.getbuffer(), uploaded_file.type)}
                response = requests.post(
                    f"{BACKEND_URL}/api/documents/",
                    files=files
                )
                
                if response.status_code == 200:
                    result = response.json()
                    st.sidebar.success(f"✅ Document uploaded!")
                    # st.sidebar.caption(f"Extracted {result['text_length']} characters")
                    st.session_state.uploader_key = f"uploader_{int(time.time() * 1000)}"  # unique timestamp
                    st.rerun()
                else:
                    st.sidebar.error(f"Upload failed: {response.json().get('error', 'Unknown error')}")
            except Exception as e:
                st.sidebar.error(f"Error: {str(e)}")

# Main chat area
st.subheader("💬 Chat")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "used_documents" in message:
            if message["used_documents"]:
                st.caption(f"📚 Using: {', '.join(message['used_documents'])}")

# Load chat history from backend
def load_chat_history():
    """Fetch chat history from the backend"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/chats/")
        if response.status_code == 200:
            chats = response.json().get("chat_history", [])
            return chats
    except Exception as e:
        st.error(f"Failed to load chat history: {str(e)}")
    return []

# Chat input
user_input = st.chat_input("Ask me anything about your documents...")

if user_input:
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("assistant"):
    # Send query to backend
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/api/chats/",
                    json={"message": user_input}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    assistant_response = result.get("response", "No response generated")
                    used_documents = result.get("used_documents", 0)
                    
                    # Display assistant response
                    st.markdown(assistant_response)                    
                    if used_documents > 0:
                        st.caption(f"📚 Used {', '.join(used_documents)} document(s) for this answer")
                    
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": assistant_response,
                        "used_documents": [doc for doc in documents[:used_documents]]
                    })
                else:
                    st.error(f"Error: {response.json().get('error', 'Unknown error')}")
            except Exception as e:
                st.error(f"Failed to get response: {str(e)}")

# Chat management in sidebar
chat_history = load_chat_history()
if chat_history:
    st.sidebar.divider()
    st.sidebar.subheader("💬 CHAT HISTORY")
    st.sidebar.markdown("Manage your chat history below.")
    with st.sidebar.expander(f"View Chat History ({len(chat_history)})", expanded=True):
        for chat in chat_history:
            st.caption(f"**{chat['role'].capitalize()}**: {chat['message']}")
        
    if st.sidebar.button("🗑️ Clear Chat History", use_container_width=True):
        try:
            response = requests.delete(f"{BACKEND_URL}/api/chats/")
            if response.status_code == 200:
                st.session_state.messages = []
                st.sidebar.success("Chat cleared!")
                st.rerun()
            else:
                st.sidebar.error("Failed to clear chat")
        except Exception as e:
            st.sidebar.error(f"Error: {str(e)}")

# Footer
st.divider()
st.caption("💡 Tip: Upload PDF, Word, CSV, or image files. The chatbot will analyze them and answer your questions based on the content.")
