import streamlit as st
import pandas as pd
import gspread
import os
import json
from gspread_dataframe import set_with_dataframe
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

# Load Font Awesome CSS
st.markdown('<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet">', unsafe_allow_html=True)

# Add GitHub icon as a link
st.markdown("""
    <style>
    .icon {
        font-size: 24px;
        margin-right: 10px;
    }
    .icon-link {
        text-decoration: none;
        color: black;
    }
    </style>
    <a class="icon-link" href="https://github.com/mmm-byte/Streamlits_Projects.git" target="_blank">
        <i class="fab fa-github icon"></i>
    </a>
    <a class="icon-link" href="https://github.com/mmm-byte/Streamlits_Projects/stargazers" target="_blank">
        <i class="far fa-star icon"></i>
    </a>
""", unsafe_allow_html=True)
    
st.title("Volunteer Feedback Survey")

# Add a header for the section with questions
st.header("Please provide your responses to the following questions")

# Load the credentials from environment variable
google_credentials = st.secrets["GOOGLE_CREDENTIALS"] 

# Define the questions for each language
questions = {
    "en": ["What is your name", "This training is relevant to my needs and/or interests?", "I have learnt new skills and/or knowledge through this training?","I can describe and explain what I learnt at this training to others?","I can apply what I have learnt to improve my work and/or my organisation?","This training will enable me to make positive changes to my organisation, sector and/or society?","Please list 3 new skills or knowledge you have learnt from this training","Please describe how you can apply what you have learnt to improve your work or benefit others","How do you plan to share your learning with others","If you did not agree with any of the statements from Q5, please feel free to share why as we would like to understand the challenges involved","Are you a repeat participant.","When I apply what I learn, my clients and/or my community experience positive change?","If applicable, please describe the positive changes that have occurred after you applied what you learnt","I am satisfied with the administrative and logistical support provided?","I am satisfied with the quality of this training?","My trainers were knowledgeable and professional?","The training formats and learning activities were engaging and effective?","Are there any other topics that you would like to learn about that was not covered during this training","If your experience could be improved or if you have any other comments and suggestions, please share it with us so that we can do better","The programme has been useful for building cross-cultural understanding through the sharing of perspectives, insights, know-how and/or experiences?","The programme has been useful for building networks, connections and friendships with people from around the world?","The programme has been useful for inspiring or bringing people around the world together to collaborate for good?","I would recommend this programme to others?","This programme has helped me gain a better understanding of Singapore or Singaporeans?","This programme has helped me form a better impression of Singapore or Singaporeans?","This programme has inspired my interest in partnering with Singaporeans or Singapore institutions on collaborative initiatives and ventures?","This programme has inspired my interest to visit Singapore?","After participating in this SIF programme, how do you think Singapore has helped to bring people together to build compassion, social innovation, or global responsibility, We may feature your quote in our reports and promotional material","I hereby give consent for my comments to be quoted and published."],
    "ms": ["Siapa nama awak", "Latihan ini berkaitan dengan keperluan dan/atau minat saya?", "Saya telah mempelajari kemahiran dan/atau pengetahuan baharu melalui latihan ini?", "Saya boleh menerangkan dan menerangkan apa yang saya pelajari pada latihan ini kepada orang lain?", "Saya boleh menggunakan apa yang saya pelajari untuk menambah baik kerja saya dan/atau organisasi saya?", "Latihan ini akan membolehkan saya membuat perubahan positif kepada organisasi, sektor dan/atau masyarakat saya?", "Sila senaraikan 3 kemahiran atau pengetahuan baharu yang telah anda pelajari daripada latihan ini", "Sila terangkan bagaimana anda boleh menggunakan apa yang telah anda pelajari untuk menambah baik kerja anda atau memberi manfaat kepada orang lain", "Bagaimana anda merancang untuk berkongsi pembelajaran anda dengan orang lain", "Jika anda tidak bersetuju dengan mana-mana kenyataan daripada S5, sila berasa bebas untuk berkongsi sebabnya kerana kami ingin memahami cabaran yang terlibat", "Adakah anda peserta ulangan", "Apabila saya menggunakan apa yang saya pelajari, pelanggan saya dan/atau komuniti saya mengalami perubahan positif?", "Jika berkenaan, sila terangkan perubahan positif yang telah berlaku selepas anda menggunakan perkara yang anda pelajari", "Saya berpuas hati dengan sokongan pentadbiran dan logistik yang diberikan?", "Saya berpuas hati dengan kualiti latihan ini?", "Jurulatih saya berpengetahuan dan profesional?", "Format latihan dan aktiviti pembelajaran menarik dan berkesan?", "Adakah terdapat topik lain yang anda ingin pelajari yang tidak dibincangkan semasa latihan ini", "Jika pengalaman anda boleh dipertingkatkan atau jika anda mempunyai sebarang komen dan cadangan lain, sila kongsikan dengan kami supaya kami boleh melakukan yang lebih baik", "Program ini telah berguna untuk membina pemahaman silang budaya melalui perkongsian perspektif, pandangan, pengetahuan dan/atau pengalaman?", "Program ini telah berguna untuk membina rangkaian, perhubungan dan persahabatan dengan orang dari seluruh dunia?", "Program ini telah berguna untuk memberi inspirasi atau membawa orang di seluruh dunia bersama-sama untuk bekerjasama demi kebaikan?", "Saya akan mengesyorkan program ini kepada orang lain?", "Program ini telah membantu saya memperoleh pemahaman yang lebih baik tentang Singapura atau Singapura?", "Program ini telah membantu saya membentuk tanggapan yang lebih baik tentang Singapura atau Singapura?", "Program ini telah menginspirasikan minat saya untuk bekerjasama dengan warga Singapura atau institusi Singapura dalam inisiatif dan usaha sama?", "Program ini telah membangkitkan minat saya untuk melawat Singapura?", "Selepas menyertai program SIF ini, pada pendapat anda, bagaimanakah Singapura telah membantu menyatukan orang ramai untuk membina belas kasihan, inovasi sosial atau tanggungjawab global, Kami mungkin memaparkan petikan anda dalam laporan dan bahan promosi kami", "Saya dengan ini memberi kebenaran untuk komen saya dipetik dan diterbitkan"],
    "id": ["¿Cuál es tu nombre?", "¿Qué tan satisfecho estás con nuestro servicio?", "¿Algún comentario adicional?"],
    "hi": ["¿Cuál es tu nombre?", "¿Qué tan satisfecho estás con nuestro servicio?", "¿Algún comentario adicional?"],
    # Add more languages as needed
}

# Define the language options
languages = {"English": "en", "Malay": "ms","Indonesian":"id","Hindi";"hi"}  # Add more languages as needed

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
    if google_credentials:
        st.write(google_credentials)
        #credentials = json.loads(google_credentials)
        #st.write(credentials)
    
        scopes = ['https://www.googleapis.com/auth/spreadsheets',
          'https://www.googleapis.com/auth/drive']

        credentials = Credentials.from_service_account_info(google_credentials, scopes=scopes)
        gc = gspread.authorize(credentials)
        gauth = GoogleAuth()
        gauth.credentials = credentials
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
    else:
        st.error("Google credentials not found in environment variables")

# Example usage of the responses list
#st.write("Responses:", responses)

footer = """
<div style="text-align: center; font-size: medium; margin-top:50px;">
    If you find BrainGazer useful or interesting, please consider starring it on GitHub.
    <hr>
    <a href="https://github.com/mmm-byte/Streamlits_Projects.git" target="_blank">
    <img src="https://img.shields.io/github/stars/SaiJeevanPuchakayala/BrainGazer.svg?style=social" alt="GitHub stars">
  </a>
</div>
"""
st.markdown(footer, unsafe_allow_html=True)
