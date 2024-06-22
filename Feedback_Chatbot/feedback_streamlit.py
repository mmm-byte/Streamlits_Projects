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
from googletrans import Translator

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
    "ms": ["Siapa nama awak", "Latihan ini berkaitan dengan keperluan dan/atau minat saya?", "Saya telah mempelajari kemahiran dan/atau pengetahuan baharu melalui latihan ini?", "Saya boleh menerangkan dan menerangkan apa yang saya pelajari pada latihan ini kepada orang lain?", "Saya boleh menggunakan apa yang saya pelajari untuk menambah baik kerja saya dan/atau organisasi saya?", "Latihan ini akan membolehkan saya membuat perubahan positif kepada organisasi, sektor dan/atau masyarakat saya?", "Sila senaraikan 3 kemahiran atau pengetahuan baharu yang telah anda pelajari daripada latihan ini", "Sila terangkan bagaimana anda boleh menggunakan apa yang telah anda pelajari untuk menambah baik kerja anda atau memberi manfaat kepada orang lain", "Bagaimana anda merancang untuk berkongsi pembelajaran anda dengan orang lain", "Jika anda tidak bersetuju dengan mana-mana kenyataan daripada S5, sila berasa bebas untuk berkongsi sebabnya kerana kami ingin memahami cabaran yang terlibat", "Adakah anda peserta ulangan.", "Apabila saya menggunakan apa yang saya pelajari, pelanggan saya dan/atau komuniti saya mengalami perubahan positif?", "Jika berkenaan, sila terangkan perubahan positif yang telah berlaku selepas anda menggunakan perkara yang anda pelajari", "Saya berpuas hati dengan sokongan pentadbiran dan logistik yang diberikan?", "Saya berpuas hati dengan kualiti latihan ini?", "Jurulatih saya berpengetahuan dan profesional?", "Format latihan dan aktiviti pembelajaran menarik dan berkesan?", "Adakah terdapat topik lain yang anda ingin pelajari yang tidak dibincangkan semasa latihan ini", "Jika pengalaman anda boleh dipertingkatkan atau jika anda mempunyai sebarang komen dan cadangan lain, sila kongsikan dengan kami supaya kami boleh melakukan yang lebih baik", "Program ini telah berguna untuk membina pemahaman silang budaya melalui perkongsian perspektif, pandangan, pengetahuan dan/atau pengalaman?", "Program ini telah berguna untuk membina rangkaian, perhubungan dan persahabatan dengan orang dari seluruh dunia?", "Program ini telah berguna untuk memberi inspirasi atau membawa orang di seluruh dunia bersama-sama untuk bekerjasama demi kebaikan?", "Saya akan mengesyorkan program ini kepada orang lain?", "Program ini telah membantu saya memperoleh pemahaman yang lebih baik tentang Singapura atau Singapura?", "Program ini telah membantu saya membentuk tanggapan yang lebih baik tentang Singapura atau Singapura?", "Program ini telah menginspirasikan minat saya untuk bekerjasama dengan warga Singapura atau institusi Singapura dalam inisiatif dan usaha sama?", "Program ini telah membangkitkan minat saya untuk melawat Singapura?", "Selepas menyertai program SIF ini, pada pendapat anda, bagaimanakah Singapura telah membantu menyatukan orang ramai untuk membina belas kasihan, inovasi sosial atau tanggungjawab global, Kami mungkin memaparkan petikan anda dalam laporan dan bahan promosi kami", "Saya dengan ini memberi kebenaran untuk komen saya dipetik dan diterbitkan."],
    "id": ["Siapa namamu", "Pelatihan ini relevan dengan kebutuhan dan/atau minat saya?", "Saya telah mempelajari keterampilan dan/atau pengetahuan baru melalui pelatihan ini?", "Saya dapat menggambarkan dan menjelaskan apa yang saya pelajari pada pelatihan ini kepada orang lain?", "Saya dapat menerapkan apa yang telah saya pelajari untuk meningkatkan pekerjaan saya dan/atau organisasi saya?", "Pelatihan ini akan memungkinkan saya membuat perubahan positif pada organisasi, sektor dan/atau masyarakat saya?", "Silakan sebutkan 3 keterampilan atau pengetahuan baru yang Anda pelajari dari pelatihan ini", "Tolong jelaskan bagaimana Anda dapat menerapkan apa yang telah Anda pelajari untuk meningkatkan pekerjaan Anda atau bermanfaat bagi orang lain", "Bagaimana Anda berencana untuk berbagi pembelajaran Anda dengan orang lain", "Jika Anda tidak setuju dengan pernyataan apa pun dari Q5, silakan sampaikan alasannya karena kami ingin memahami tantangan yang ada", "Apakah Anda peserta berulang.", "Ketika saya menerapkan apa yang saya pelajari, klien saya dan/atau komunitas saya mengalami perubahan positif?", "Jika memungkinkan, jelaskan perubahan positif yang terjadi setelah Anda menerapkan apa yang Anda pelajari", "Saya puas dengan dukungan administratif dan logistik yang diberikan?", "Saya puas dengan kualitas pelatihan ini?", "Pelatih saya berpengetahuan luas dan profesional?", "Format pelatihan dan kegiatan pembelajaran menarik dan efektif?", "Apakah ada topik lain yang ingin Anda pelajari yang belum dibahas selama pelatihan ini", "Jika pengalaman Anda dapat ditingkatkan atau jika Anda memiliki komentar dan saran lain, silakan sampaikan kepada kami agar kami dapat berbuat lebih baik", "Apakah program ini bermanfaat untuk membangun pemahaman lintas budaya melalui pertukaran perspektif, wawasan, pengetahuan dan/atau pengalaman?", "Apakah program ini bermanfaat untuk membangun jaringan, koneksi dan persahabatan dengan orang-orang dari seluruh dunia?", "Apakah program ini bermanfaat untuk menginspirasi atau menyatukan orang-orang di seluruh dunia untuk berkolaborasi demi kebaikan?", "Saya akan merekomendasikan program ini kepada orang lain?", "Program ini telah membantu saya mendapatkan pemahaman yang lebih baik tentang Singapura atau orang Singapura?", "Program ini telah membantu saya membentuk kesan yang lebih baik tentang Singapura atau orang Singapura?", "Program ini telah menginspirasi minat saya untuk bermitra dengan warga Singapura atau institusi Singapura dalam inisiatif dan usaha kolaboratif?", "Program ini menginspirasi minat saya untuk mengunjungi Singapura?", "Setelah berpartisipasi dalam program SIF ini, menurut Anda bagaimana Singapura telah membantu menyatukan masyarakat untuk membangun kasih sayang, inovasi sosial, atau tanggung jawab global, Kami dapat menampilkan kutipan Anda dalam laporan dan materi promosi kami", "Dengan ini saya memberikan persetujuan agar komentar saya dikutip dan dipublikasikan."],
    "hi": ["आपका क्या नाम है", "क्या यह प्रशिक्षण मेरी आवश्यकताओं और/या रुचियों के लिए प्रासंगिक है?", "क्या मैंने इस प्रशिक्षण के माध्यम से नए कौशल और/या ज्ञान सीखा है?", "क्या मैं दूसरों को बता सकता हूँ कि मैंने इस प्रशिक्षण में क्या सीखा?", "क्या मैं अपने काम और/या अपने संगठन को बेहतर बनाने के लिए जो कुछ सीखा है उसे लागू कर सकता हूँ?", "क्या यह प्रशिक्षण मुझे अपने संगठन, क्षेत्र और/या समाज में सकारात्मक परिवर्तन करने में सक्षम बनाएगा?", "कृपया इस प्रशिक्षण से सीखे गए तीन नए कौशल या ज्ञान की सूची बनाएं", "कृपया बताएं कि आपने जो सीखा है उसे आप अपने काम को बेहतर बनाने या दूसरों को लाभ पहुंचाने के लिए कैसे लागू कर सकते हैं", "आप अपनी सीख को दूसरों के साथ साझा करने की योजना कैसे बनाते हैं", "यदि आप प्रश्न 5 के किसी भी कथन से सहमत नहीं हैं, तो कृपया अपने विचार साझा करें, क्योंकि हम इसमें शामिल चुनौतियों को समझना चाहते हैं।", "क्या आप बार-बार भाग लेने वाले व्यक्ति हैं.", "जब मैं सीखी हुई बातों को लागू करता हूँ, तो क्या मेरे ग्राहक और/या मेरा समुदाय सकारात्मक परिवर्तन अनुभव करता है?", "यदि लागू हो, तो कृपया बताएं कि आपने जो सीखा उसे लागू करने के बाद क्या सकारात्मक परिवर्तन हुए हैं", "क्या मैं प्रदान की गई प्रशासनिक एवं तार्किक सहायता से संतुष्ट हूं?", "क्या मैं इस प्रशिक्षण की गुणवत्ता से संतुष्ट हूँ?", "मेरे प्रशिक्षक जानकार और पेशेवर थे?", "क्या प्रशिक्षण प्रारूप और शिक्षण गतिविधियाँ आकर्षक और प्रभावी थीं?", "क्या कोई अन्य विषय है जिसके बारे में आप जानना चाहेंगे जो इस प्रशिक्षण के दौरान कवर नहीं किया गया", "यदि आपका अनुभव बेहतर हो सकता है या यदि आपके पास कोई अन्य टिप्पणी और सुझाव है, तो कृपया इसे हमारे साथ साझा करें ताकि हम बेहतर कर सकें", "यह कार्यक्रम दृष्टिकोण, अंतर्दृष्टि, जानकारी और/या अनुभवों के आदान-प्रदान के माध्यम से अंतर-सांस्कृतिक समझ बनाने के लिए उपयोगी रहा है।?", "यह कार्यक्रम विश्व भर के लोगों के साथ नेटवर्क, सम्पर्क और मित्रता बनाने के लिए उपयोगी रहा है।?", "क्या यह कार्यक्रम दुनिया भर के लोगों को अच्छे कार्यों के लिए सहयोग करने हेतु प्रेरित करने या एक साथ लाने में उपयोगी रहा है?", "मैं दूसरों को इस कार्यक्रम की सिफारिश करूंगा?", "इस कार्यक्रम से मुझे सिंगापुर या सिंगापुरवासियों को बेहतर ढंग से समझने में मदद मिली है।?", "इस कार्यक्रम ने मुझे सिंगापुर या सिंगापुरवासियों के बारे में बेहतर धारणा बनाने में मदद की है।?", "इस कार्यक्रम ने सहयोगात्मक पहलों और उद्यमों पर सिंगापुर या सिंगापुर संस्थानों के साथ साझेदारी करने में मेरी रुचि को प्रेरित किया है।?", "इस कार्यक्रम ने सिंगापुर जाने के लिए मेरी रुचि को प्रेरित किया है?", "इस एसआईएफ कार्यक्रम में भाग लेने के बाद, आपको क्या लगता है कि सिंगापुर ने लोगों को करुणा, सामाजिक नवाचार या वैश्विक जिम्मेदारी बनाने के लिए एक साथ लाने में कैसे मदद की है, हम आपकी रिपोर्ट को अपनी रिपोर्ट और प्रचार सामग्री में शामिल कर सकते हैं।", "मैं अपनी टिप्पणियों को उद्धृत और प्रकाशित करने की सहमति देता हूं."],
    # Add more languages as needed
}

#Define the answers for each language
answers = {
    "en": ["Very Satisfied", "Satisfied", "Neutral", "Dissatisfied", "Very Dissatisfied"],
    "ms":["Sangat Puas Hati", "Puas Hati", "Neutral", "Tidak Puas Hati", "Sangat Tidak Puas Hati"],
    "id":["Sangat Puas", "Puas", "Netral", "Tidak Puas", "Sangat Tidak Puas"],
    "hi":["बहुत संतुष्ट", "संतुष्ट", "तटस्थ", "असंतुष्ट", "बहुत असंतुष्ट"],
}

#Deine the answers for each language
answers1 = {
    "en": ["Yes", "No"],
    "ms":["Ya","Tidak"],
    "id":["Ya","Tidak"],
    "hi":["हां", "नहीं"],
}

# Define the language options
languages = {"English": "en", "Malay": "ms","Indonesian":"id","Hindi":"hi"}  # Add more languages as needed

# Select language
selected_language = st.selectbox("Select Language", list(languages.keys()))
selected_lang_code = languages[selected_language]

# Translate is defined to google translator
trans = Translator()

# Display questions in the selected language
responses = []
responses_original = []
for question in questions[selected_lang_code]:
    if "?" in question:
        response = st.selectbox(question, answers[selected_lang_code])
    elif "." in question:
        response = st.selectbox(question, answers1[selected_lang_code])
    else:
        response = st.text_input(question)

    # Check if the response is empty
    responses_original.append(response)
    if response:
        print("here")
        translated = trans.translate(response).text
        responses.append(translated)
    else:
        print("not here")
        responses.append(response)
    

# Submit button
if st.button("Submit"):
    if google_credentials:
        #st.write(google_credentials)
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
        worksheet2 = gs.worksheet('Sheet2')

        # Find the next empty row
        next_empty_row = len(worksheet1.col_values(1)) + 1
        next_empty_row_org = len(worksheet2.col_values(1)) + 1
    
        # Append the responses to the next empty row
        worksheet1.insert_row(responses, next_empty_row)
        worksheet2.insert_row(responses_original, next_empty_row_org)
    
        st.success('Responses submitted successfully!')
    else:
        st.error("Google credentials not found in environment variables")

# Example usage of the responses list
st.write("Responses:", responses)

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
