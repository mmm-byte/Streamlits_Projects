import streamlit as st

class FeedbackChatbot:
    def __init__(self):
        self.feedback = []
        self.questions = [
            {"question": "Did you find our service helpful? (yes/no)", "type": "yesno"},
            {"question": "How would you rate our service? (very good/good/bad)", "type": "rating"},
            {"question": "Please provide any additional feedback:", "type": "string"}
        ]

    def greet(self):
        return "Hello! Thank you for using our service. We'd love to hear your feedback."

    def ask_question(self, question):
        return question

    def receive_feedback(self, user_input, question_type):
        if question_type == "yesno":
            if user_input.lower() in ["yes", "no"]:
                self.feedback.append(user_input)
                return "Thank you!"
            else:
                return "Please answer with 'yes' or 'no'."
        elif question_type == "rating":
            if user_input.lower() in ["very good", "good", "bad"]:
                self.feedback.append(user_input)
                return "Thank you!"
            else:
                return "Please answer with 'very good', 'good', or 'bad'."
        elif question_type == "string":
            self.feedback.append(user_input)
            return "Thank you for your detailed feedback!"

    def thank_you(self):
        return "Thanks for your time! Have a great day!"

    def run(self):
        st.write(self.greet())
        for question in self.questions:
            while True:
                user_input = st.text_input(self.ask_question(question["question"]), key=question["question"])
                if user_input:
                    response = self.receive_feedback(user_input, question["type"])
                    st.write(response)
                    if response == "Thank you!":
                        break
        st.write(self.thank_you())

# Create an instance of the chatbot and run it
chatbot = FeedbackChatbot()
chatbot.run()
