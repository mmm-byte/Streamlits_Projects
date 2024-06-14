import streamlit as st
from googletrans import Translator
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Initialize the translator
translator = Translator()

# Define the questions
questions = {
    "en": ["What is your name?", "How satisfied are you with our service?", "Any additional comments?"],
    "es": ["¿Cuál es tu nombre?", "¿Qué tan satisfecho estás con nuestro servicio?", "¿Algún comentario adicional?"],
    # Add more languages as needed
}

# Define the language options
languages = {"English": "en", "Spanish": "es"}  # Add more languages as needed

# Select language
selected_language = st.selectbox("Select Language", list(languages.keys()))
selected_lang_code = languages[selected_language]

# Display questions in the selected language
responses = []
for question in questions[selected_lang_code]:
    if "satisfied" in question:
        response = st.selectbox(question, ["Very Satisfied", "Satisfied", "Neutral", "Dissatisfied", "Very Dissatisfied"])
    else:
        response = st.text_input(question)
    responses.append(response)

# Submit button
if st.button("Submit"):
    # Google Sheets API setup
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = None

    if 'token.json' not in st.session_state:
        flow = InstalledAppFlow.from_client_secrets_file("./Feedback_Chatbot/credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)
        st.session_state['./Feedback_Chatbot/token.json'] = creds.to_json()
    else:
        creds = Credentials.from_authorized_user_info(st.session_state['./Feedback_Chatbot/token.json'])

    # Authenticate and open the Google Sheet
    client = gspread.authorize(creds)
    sheet = client.open("Feedback Responses").sheet1

    # Append the new responses
    sheet.append_row(responses)

    st.success("Thank you for your feedback!")

# Run the app with the command `streamlit run feedback_form.py`
