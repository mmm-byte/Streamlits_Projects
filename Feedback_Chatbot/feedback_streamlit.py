import streamlit as st
import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
from google.oauth2.service_account import Credentials
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

# Define the questions for each language
questions = {
    "en": ["What is your name", "This training is relevant to my needs and/or interests?", "I have learnt new skills and/or knowledge through this training?","I can describe and explain what I learnt at this training to others?","I can apply what I have learnt to improve my work and/or my organisation?","This training will enable me to make positive changes to my organisation, sector and/or society?","Please list 3 new skills or knowledge you have learnt from this training","Please describe how you can apply what you have learnt to improve your work or benefit others","How do you plan to share your learning with others","If you did not agree with any of the statements from Q5, please feel free to share why as we would like to understand the challenges involved","Are you a repeat participant.","When I apply what I learn, my clients and/or my community experience positive change?","If applicable, please describe the positive changes that have occurred after you applied what you learnt","I am satisfied with the administrative and logistical support provided?","I am satisfied with the quality of this training?","My trainers were knowledgeable and professional?","The training formats and learning activities were engaging and effective?","Are there any other topics that you would like to learn about that was not covered during this training","If your experience could be improved or if you have any other comments and suggestions, please share it with us so that we can do better","The programme has been useful for building cross-cultural understanding through the sharing of perspectives, insights, know-how and/or experiences?","The programme has been useful for building networks, connections and friendships with people from around the world?","The programme has been useful for inspiring or bringing people around the world together to collaborate for good?","I would recommend this programme to others?","This programme has helped me gain a better understanding of Singapore or Singaporeans?","This programme has helped me form a better impression of Singapore or Singaporeans?","This programme has inspired my interest in partnering with Singaporeans or Singapore institutions on collaborative initiatives and ventures?","This programme has inspired my interest to visit Singapore?","After participating in this SIF programme, how do you think Singapore has helped to bring people together to build compassion, social innovation, or global responsibility, We may feature your quote in our reports and promotional material","I hereby give consent for my comments to be quoted and published."],
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
    if "?" in question:
        response = st.selectbox(question, ["Very Satisfied", "Satisfied", "Neutral", "Dissatisfied", "Very Dissatisfied"])
    elif "." in question:
        response = st.selectbox(question, ["Yes", "No"])
    else:
        response = st.text_input(question)
    responses.append(response)

# Submit button
if st.button("Submit"):
    scopes = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']
    credentials = Credentials.from_service_account_file('./Feedback_Chatbot/credentials.json', scopes=scopes)
    gc = gspread.authorize(credentials)
    gauth = GoogleAuth()
    drive = GoogleDrive(gauth)
    
    # open a google sheet
    gs = gc.open_by_url('https://docs.google.com/spreadsheets/d/178sSyO5YpLNOVz8XtZJTif6Vc07-K7Nncjp56TB3qb8/edit?usp=sharing')
    
    # select a work sheet from its name
    worksheet1 = gs.worksheet('Sheet1')

    # Find the next empty row
    next_empty_row = len(worksheet1.col_values(1)) + 1
    
    # Append the responses to the next empty row
    worksheet1.insert_row(responses, next_empty_row)
    
    st.success('Responses submitted successfully!')

# Example usage of the responses list
st.write("Responses:", responses)

