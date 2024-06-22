import streamlit as st
import google.generativeai as genai

# Secret value
api_credentials = st.secrets['my_api_key']

# Title
st.title('Welcome to SIF Feedback Chatbot')

# Function to display the chat message with options as buttons
def chat_message_with_buttons(content, options):
    st.write(content)
    selected_option = None
    button_cols = st.columns(len(options))
    for idx, option in enumerate(options):
        if button_cols[idx].button(option):
            selected_option = option
    return selected_option

# Function to display the chat message with multi-line text input
def chat_message_with_text_input(content):
    st.write(content)
    user_input = st.text_area("Your input:")
    return user_input

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "How are you doing?"},
        {"role": "assistant", "content": "Is the feedback nice?"},
        {"role": "assistant", "content": "Anything to add?"}
    ]
    st.session_state["answers"] = []
    st.session_state["current_question"] = 0

genai.configure(api_key=api_credentials)
model = genai.GenerativeModel('gemini-1.5-flash')

# Display messages and collect user responses
if st.session_state["current_question"] < len(st.session_state["messages"]):
    current_msg = st.session_state["messages"][st.session_state["current_question"]]
    
    if current_msg["role"] == "assistant":
        if st.session_state["current_question"] == 0:
            options = ["Excellent", "Good", "Better", "Bad"]
            selected_option = chat_message_with_buttons(current_msg["content"], options)
            if selected_option:
                st.session_state["answers"].append(selected_option)
                st.session_state["current_question"] += 1
        elif st.session_state["current_question"] == 1:
            options = ["Yes", "No"]
            selected_option = chat_message_with_buttons(current_msg["content"], options)
            if selected_option:
                st.session_state["answers"].append(selected_option)
                st.session_state["current_question"] += 1
        elif st.session_state["current_question"] == 2:
            user_input = chat_message_with_text_input(current_msg["content"])
            if user_input:
                st.session_state["answers"].append(user_input)
                st.session_state["current_question"] += 1

# Display user inputs as chat messages
for idx, answer in enumerate(st.session_state.answers):
    st.chat_message("user").write(answer)

# Hide the default chat input box
st.markdown(
    """
    <style>
    .stTextInput, .stTextArea, .stTextInput div[data-baseweb="input"], .stTextArea div[data-baseweb="textarea"] {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Show options at the position of the chat input box
if st.session_state["current_question"] < len(st.session_state["messages"]):
    current_msg = st.session_state["messages"][st.session_state["current_question"]]
    
    if current_msg["role"] == "assistant":
        if st.session_state["current_question"] == 0:
            options = ["Excellent", "Good", "Better", "Bad"]
            selected_option = chat_message_with_buttons(current_msg["content"], options)
            if selected_option:
                st.session_state["answers"].append(selected_option)
                st.session_state["current_question"] += 1
        elif st.session_state["current_question"] == 1:
            options = ["Yes", "No"]
            selected_option = chat_message_with_buttons(current_msg["content"], options)
            if selected_option:
                st.session_state["answers"].append(selected_option)
                st.session_state["current_question"] += 1
        elif st.session_state["current_question"] == 2:
            user_input = chat_message_with_text_input(current_msg["content"])
            if user_input:
                st.session_state["answers"].append(user_input)
                st.session_state["current_question"] += 1
