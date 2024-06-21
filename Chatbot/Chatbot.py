import streamlit as st

class FeedbackChatbot:
    def __init__(self):
        self.feedback = []
        self.questions = [
            {"question": "Did you find our service helpful?", "type": "yesno", "options": ["Yes", "No"]},
            {"question": "How would you rate our service?", "type": "rating", "options": ["Very Good", "Good", "Bad"]},
            {"question": "Please provide any additional feedback:", "type": "string"}
        ]
        self.current_question_index = 0

    def greet(self):
        return "Hi! Great day. Thanks for your feedback."

    def ask_question(self):
        return self.questions[self.current_question_index]["question"]

    def receive_feedback(self, user_input):
        question_type = self.questions[self.current_question_index]["type"]
        if question_type in ["yesno", "rating"]:
            self.feedback.append(user_input)
        elif question_type == "string":
            self.feedback.append(user_input)

    def next_question(self):
        self.current_question_index += 1

    def run(self):
        st.write(self.greet())
        while self.current_question_index < len(self.questions):
            st.text_area("Chatbot:", value=self.ask_question(), height=100)
            user_input = st.text_input("You:", key=str(self.current_question_index))
            if st.button("Send"):
                self.receive_feedback(user_input)
                self.next_question()
        
        st.write("Thank you for your time! Have a great day.")

# Create an instance of the chatbot and run it
chatbot = FeedbackChatbot()
chatbot.run()
