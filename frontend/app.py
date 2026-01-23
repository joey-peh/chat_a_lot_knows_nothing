import streamlit as st
import requests  # To interact with the backend API

st.title("Chat a lot.. knows nothing")

st.warning('Please upload documents to teach me something..', icon="⚠️")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "file_details" in message:
            st.write(f"Uploaded file: {message['file_details']['name']}")

# Accept user input and files
user_input = st.text_input("Say something:")

uploaded_files = st.file_uploader(
    "Upload a file", type=["csv", "png", "jpg", "jpeg", "pdf"], accept_multiple_files=True
)

if user_input or uploaded_files:
    # Handle the user's message and uploaded files
    user_message = user_input

    # Display user message in the chat
    with st.chat_message("user"):
        st.markdown(user_message)
        file_details_list = []

        # Send uploaded files to the backend for processing
        for file in uploaded_files:
            st.write(f"Uploaded file: {file.name}")
            file_details = {"name": file.name, "type": file.type, "size": file.size}
            file_details_list.append(file_details)
            
            # Send the file to the backend API (replace with your actual API URL)
            backend_url = "http://localhost:8000/api/process_document/"  # Replace with actual URL

            files = {'file': (file.name, file, file.type)}
            response = requests.post(backend_url, files=files)

            if response.status_code == 200:
                st.write(f"File processed successfully: {file.name}")
                st.write(f"Processed data: {response.json()}")
            else:
                st.error(f"Failed to process file: {file.name}")

        # Append file details to session state for future use
        st.session_state.messages.append({"role": "user", "content": user_message, "file_details": file_details_list})

    # Simulate assistant response (replace with your LLM logic)
    with st.chat_message("assistant"):
        # Simple response
        response = f"You said: '{user_message}'. You uploaded {len(uploaded_files)} file(s)."
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
