import streamlit as st
import pandas as pd

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
            # Example processing for a CSV file
            if message['file_details']['type'] == 'text/csv':
                df = pd.read_csv(message['file_details'])
                st.dataframe(df.head())


# Accept user input and files
prompt_container = st.chat_input(
    "Say something and/or attach a file",
    accept_file=True,
    file_type=["csv", "png", "jpg", "jpeg", "pdf"]
)

if prompt_container:
    # Handle the user's message
    user_message = prompt_container.text
    # Handle the user's uploaded files (it's a list even for single file mode)
    uploaded_files = prompt_container.files
    
    # Display user message and files in the chat
    with st.chat_message("user"):
        st.markdown(user_message)
        for file in uploaded_files:
            st.write(f"Uploaded file: {file.name}")
            # Add file details to session state for later display if needed
            file_details = {"name": file.name, "type": file.type, "size": file.size, "data": file.getvalue()}
            # Note: Storing large file data in session_state can impact performance.
            # A common pattern is to process the file immediately and store only the results/embeddings.

    # Append to chat history (simple text-based history example)
    st.session_state.messages.append({"role": "user", "content": user_message})

    # Simulate assistant response (replace with your LLM logic)
    with st.chat_message("assistant"):
        response = f"You said: '{user_message}'. You uploaded {len(uploaded_files)} file(s)."
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

