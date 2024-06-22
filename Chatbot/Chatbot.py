import streamlit as st
import google.generativeai as genai

# Secret value
api_credentials = st.secrets['my_api_key']

# Title
st.title('Welcome to SIF Feedback Chatbot')

# Function to display the chat message with options as buttons
def chat_message_with_buttons(role, content, options):
    st.chat_message(role).write(content)
    selected_option = None
    if role == "user":
        button_cols = st.columns(len(options))
        for idx, option in enumerate(options):
            if button_cols[idx].button(option):
                selected_option = option
    return selected_option

# Function to display the chat message with multi-line text input
def chat_message_with_text_input(role, content):
    st.chat_message(role).write(content)
    user_input = None
    if role == "user":
        user_input = st.text_area("Your input:")
    return user_input

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "How are you doing?"},
        {"role": "assistant", "content": "Is the feedback nice?"},
        {"role": "assistant", "content": "Anything to add?"}
    ]
    st.session_state["answers"] = []

genai.configure(api_key=api_credentials)
model = genai.GenerativeModel('gemini-1.5-flash')

# Iterate through the messages and collect user responses
for i, msg in enumerate(st.session_state.messages):
    if msg["role"] == "assistant":
        if i == 0:
            options = ["Excellent", "Good", "Better", "Bad"]
            selected_option = chat_message_with_buttons("user", msg["content"], options)
            if selected_option:
                st.session_state.answers.append(selected_option)
        elif i == 1:
            options = ["Yes", "No"]
            selected_option = chat_message_with_buttons("user", msg["content"], options)
            if selected_option:
                st.session_state.answers.append(selected_option)
        elif i == 2:
            user_input = chat_message_with_text_input("user", msg["content"])
            if user_input:
                st.session_state.answers.append(user_input)

# Display user inputs
for idx, answer in enumerate(st.session_state.answers):
    st.chat_message("user").write(answer)

# Handle additional chat input and response
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = model.generate_content(prompt, stream=True)
    resp = ''
    for chunk in response:
        resp += chunk.text
    st.session_state.messages.append({"role": "assistant", "content": resp})
    st.chat_message("assistant").write(resp)
