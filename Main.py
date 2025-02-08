import streamlit as st
from AI import AI;

# Initialize the AI instance only once
if "ai" not in st.session_state:
    st.session_state.ai = AI()

st.title("Memory Bot")

# # File uploader for text documents
# uploaded_file = st.file_uploader("Choose a text file", type="pdf")

# if uploaded_file is not None:
#     # Read the content of the uploaded file
#     content = uploaded_file.read().decode("utf-8")

#     # Display the content in a text box
#     st.text_area("File Content", content, height=300)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    if prompt == "exit":
        st.session_state.ai.save()
    else:
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        response = f"Bot: {st.session_state.ai.getAnswer(prompt)}"
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
