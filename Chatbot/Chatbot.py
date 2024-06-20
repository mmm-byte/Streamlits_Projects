import openai
import streamlit as st
import pandas as pd

# Set your OpenAI API key
openai.api_key = 'sk-personal2-6toXk76rHSkvkBuZzhvJT3BlbkFJgXw8BOhQhlQBCseZhYlV'

# Initialize session state for storing feedback
if 'feedback' not in st.session_state:
    st.session_state['feedback'] = []

# Function to generate chatbot response
def generate_response(user_input):
    response = openai.Completion.create(
        engine="davinci",
        prompt=user_input,
        max_tokens=150
    )
    message = response.choices[0].text.strip()
    return message

# Function to collect feedback
def collect_feedback(questions):
    responses = []
    for question in questions:
        response = st.text_input(question)
        if response:
            responses.append(response)
    return responses

# Main chatbot interaction
def chatbot():
    st.title("Feedback Chatbot")
    st.write("Welcome! Please interact with the chatbot and provide your feedback.")

    user_input = st.text_input("You:", "")
    if user_input:
        response = generate_response(user_input)
        st.session_state['feedback'].append({'user': user_input, 'bot': response})
        st.write("Bot:", response)

    # Display previous conversation
    st.write("Conversation History:")
    for convo in st.session_state['feedback']:
        st.write(f"You: {convo['user']}")
        st.write(f"Bot: {convo['bot']}")

    st.write("Please provide your feedback:")
    feedback_questions = [
        "How do you rate your experience?",
        "Any suggestions for improvement?",
        "Would you recommend this chatbot to others?"
    ]
    feedback_responses = collect_feedback(feedback_questions)

    if st.button("Submit Feedback"):
        for question, response in zip(feedback_questions, feedback_responses):
            st.session_state['feedback'].append({'question': question, 'response': response})
        st.write("Thank you for your feedback!")

    # Option to download feedback as CSV
    if st.button("Download Feedback"):
        df = pd.DataFrame(st.session_state['feedback'])
        df.to_csv('feedback.csv', index=False)
        st.write("Feedback saved to feedback.csv")

# Run the chatbot function
if __name__ == "__main__":
    chatbot()
