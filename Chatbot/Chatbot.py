import streamlit as st

class FeedbackChatbot:
    def __init__(self):
        self.feedback = []
        self.questions = [
            {"question": "Did you find our service helpful?", "type": "yesno", "options": ["Yes", "No"]},
            {"question": "How would you rate our service?", "type": "rating", "options": ["Very Good", "Good", "Bad"]},
            {"question": "Please provide any additional feedback:", "type": "string"}
        ]

    def greet(self):
        return "Hello! Thank you for using our service. We'd love to hear your feedback."

    def ask_question(self, question):
        return question

    def receive_feedback(self, user_input, question_type):
        if question_type in ["yesno", "rating"]:
            self.feedback.append(user_input)
            return "Thank you!"
        elif question_type == "string":
            self.feedback.append(user_input)
            return "Thank you for your detailed feedback!"

    def thank_you(self):
        return "Thanks for your time! Have a great day!"

    def run(self):
        st.write(self.greet())
        for question in self.questions:
            if question["type"] == "yesno" or question["type"] == "rating":
                user_input = st.selectbox(self.ask_question(question["question"]), question["options"], key=question["question"])
            elif question["type"] == "string":
                user_input = st.text_area(self.ask_question(question["question"]), key=question["question"])

            if user_input:
                response = self.receive_feedback(user_input, question["type"])
                st.write(response)
        
        st.write(self.thank_you())

# Create an instance of the chatbot and run it
chatbot = FeedbackChatbot()
chatbot.run()
