import streamlit as st
from llama_index.llms.ollama import Ollama
from llama_index.core.llms import ChatMessage

# --- Streamlit Configuration ---
st.set_page_config(page_title="Llama3 Chatbot (Ollama)", layout="centered")

st.title("Llama3 Chatbot")

# --- Ollama Model Initialization ---
# Ensure Ollama is running and you've run 'ollama pull llama3'
try:
    llm = Ollama(model="llama3")
except Exception as e:
    st.error(f"Error initializing Ollama. Please check if Ollama is running and if the 'llama3' model is available. Error: {e}")
    st.stop() # Stop execution if Ollama can't be initialized

# --- Chat History Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Display Previous Messages ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- User Input ---
if prompt := st.chat_input("Say something..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Build the list of ChatMessage for LlamaIndex
                messages_for_llm = [
                    ChatMessage(role=m["role"], content=m["content"])
                    for m in st.session_state.messages
                ]

                # Call the Llama3 model via Ollama
                response = llm.chat(messages_for_llm)
                assistant_response = response.message.content

                st.markdown(assistant_response)
                st.session_state.messages.append({"role": "assistant", "content": assistant_response})

            except Exception as e:
                st.error(f"Error generating response from Llama3: {e}")
                st.session_state.messages.append({"role": "assistant", "content": "Sorry, an error occurred while processing your request."})

# Clear Chat History Button
if len(st.session_state.messages) > 0:
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.success("Chat history cleared!")
        st.rerun() # Rerun the app to update the display