import streamlit as st

# Title
st.title('Welcome to SIF Feedback Chatbot')

# Example questions and answers for demonstration purposes
questions = {
    "en": [
        "How are you doing?",
        "Is the feedback nice.",
        "Anything to add"
    ]
}

answers = {
    "en": ["Excellent", "Good", "Better", "Bad"]
}

answers1 = {
    "en": ["Yes", "No"]
}

# Select language code
selected_lang_code = "en"

# Function to display the chat message with options as buttons
def chat_message_with_buttons(content, options):
    st.write(content)
    selected_option = None
    button_cols = st.columns(len(options))
    for idx, option in enumerate(options):
        if button_cols[idx].button(option):
            selected_option = option
    return selected_option

# Function to display the chat message with text input
def chat_message_with_text_input(content):
    st.write(content)
    user_input = st.text_input("Your input:")
    return user_input

# Initialize session state
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
    st.session_state.responses = []

# Display previous questions and responses
for i in range(st.session_state.current_question):
    st.chat_message("assistant").write(questions[selected_lang_code][i])
    st.chat_message("user").write(st.session_state.responses[i])

# Display current question and collect response
if st.session_state.current_question < len(questions[selected_lang_code]):
    question = questions[selected_lang_code][st.session_state.current_question]
    
    if "?" in question:
        response = chat_message_with_buttons(question, answers[selected_lang_code])
    elif "." in question:
        response = chat_message_with_buttons(question, answers1[selected_lang_code])
    else:
        response = chat_message_with_text_input(question)

    if response:
        st.session_state.responses.append(response)
        st.session_state.current_question += 1
        st.experimental_rerun()  # Rerun to display the next question

# Optionally, display a thank you message after all questions are answered
if st.session_state.current_question == len(questions[selected_lang_code]):
    st.write("Thank you for your feedback!")
