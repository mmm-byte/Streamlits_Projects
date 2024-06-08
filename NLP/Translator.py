import tempfile
import streamlit as st
from googletrans import Translator
import pandas as pd
import os

# Function to detect language
def detect_language(text):
    translator = Translator()
    return translator.detect(text).lang

# Function to translate text
def translate_text(text, dest_lang, src_lang):
    translator = Translator()
    return translator.translate(text, dest=dest_lang, src=src_lang).text

# Function to translate file
def translate_file(file_path, dest_lang, src_lang):
    if file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path)
        df = df.applymap(lambda x: translate_text(str(x), dest_lang, src_lang))
        df.to_excel("translated.xlsx", index=False)
    elif file_path.endswith('.pptx') or file_path.endswith('.docx') or file_path.endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            translated_text = translate_text(text, dest_lang, src_lang)
        with open("translated.txt", 'w', encoding='utf-8') as file:
            file.write(translated_text)

# Main function
def main():
    st.title("Language Translator")

    # Input options
    input_type = st.radio("Select input type:", ("Text", "Upload File"))

    # Get user input
    if input_type == "Text":
        text = st.text_area("Enter text to translate:")
        src_lang = st.selectbox("Select input language:", ["Auto", "English", "French", "Spanish", "Chinese", "Japanese", "Korean", "Hindi", "Arabic", "Bengali", "Russian", "Punjabi", "Turkish", "Vietnamese", "Marathi", "Telugu", "Tamil", "Urdu", "Gujarati", "Kannada", "Malayalam", "Odia", "Thai", "Malay", "Indonesian", "Filipino", "Sinhala", "Malay", "Indonesian", "Bengali", "Sinhala", "Vietnamese", "Mandarin Chinese", "Cantonese", "Hokkien", "Hakka", "Tamil", "Thai", "Sinhala", "Tamil", "Vietnamese", "Mandarin Chinese", "Cantonese", "Shanghainese", "Hokkien", "Hakka", "Japanese"])  # Add more languages as needed
        dest_lang = st.selectbox("Select output language:", ["English", "French", "Spanish", "Chinese", "Japanese", "Korean", "Hindi", "Arabic", "Bengali", "Russian", "Punjabi", "Turkish", "Vietnamese", "Marathi", "Telugu", "Tamil", "Urdu", "Gujarati", "Kannada", "Malayalam", "Odia", "Thai", "Malay", "Indonesian", "Filipino", "Sinhala", "Malay", "Indonesian", "Bengali", "Sinhala", "Vietnamese", "Mandarin Chinese", "Cantonese", "Hokkien", "Hakka", "Tamil", "Thai", "Sinhala", "Tamil", "Vietnamese", "Mandarin Chinese", "Cantonese", "Shanghainese", "Hokkien", "Hakka", "Japanese"])  # Add more languages as needed
        if st.button("Translate"):
            if src_lang == "Auto":
                src_lang = detect_language(text)
            translated_text = translate_text(text, dest_lang.lower(), src_lang.lower())
            st.write("Translated Text:")
            st.write(translated_text)
            #st.markdown(get_binary_file_downloader_html('translated.txt', 'Translated Text'), unsafe_allow_html=True)

    elif input_type == "Upload File":
        file = st.file_uploader("Upload a file:", type=['xlsx', 'pptx', 'docx', 'txt'])
        if file is not None:
            temp = tempfile.mkdtemp()
            with open(os.path.join(temp, file.name), "wb") as f:
                f.write(file.getvalue())
            file_path = os.path.join("temp", file.name)
            print("File path:", file_path)
            src_lang = st.selectbox("Select input language:", ["Auto", "English", "French", "Spanish", "Chinese", "Japanese", "Korean", "Hindi", "Arabic", "Bengali", "Russian", "Punjabi", "Turkish", "Vietnamese", "Marathi", "Telugu", "Tamil", "Urdu", "Gujarati", "Kannada", "Malayalam", "Odia", "Thai", "Malay", "Indonesian", "Filipino", "Sinhala", "Malay", "Indonesian", "Bengali", "Sinhala", "Vietnamese", "Mandarin Chinese", "Cantonese", "Hokkien", "Hakka", "Tamil", "Thai", "Sinhala", "Tamil", "Vietnamese", "Mandarin Chinese", "Cantonese", "Shanghainese", "Hokkien", "Hakka", "Japanese"])  # Add more languages as needed
            dest_lang = st.selectbox("Select output language:", ["English", "French", "Spanish", "Chinese", "Japanese", "Korean", "Hindi", "Arabic", "Bengali", "Russian", "Punjabi", "Turkish", "Vietnamese", "Marathi", "Telugu", "Tamil", "Urdu", "Gujarati", "Kannada", "Malayalam", "Odia", "Thai", "Malay", "Indonesian", "Filipino", "Sinhala", "Malay", "Indonesian", "Bengali", "Sinhala", "Vietnamese", "Mandarin Chinese", "Cantonese", "Hokkien", "Hakka", "Tamil", "Thai", "Sinhala", "Tamil", "Vietnamese", "Mandarin Chinese", "Cantonese", "Shanghainese", "Hokkien", "Hakka", "Japanese"])  # Add more languages as needed
            if st.button("Translate"):
                if src_lang == "Auto":
                    with open(file_path, 'r', encoding='utf-8') as f:
                        text = f.read()
                        src_lang = detect_language(text)
                translate_file(file_path, dest_lang.lower(), src_lang.lower())
                st.write("File Translated Successfully!")
                st.markdown(get_binary_file_downloader_html('translated.txt', 'Translated File'), unsafe_allow_html=True)
                os.rmdir(temp)

def get_binary_file_downloader_html(bin_file, file_label='File'):
    with open(bin_file, 'rb') as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{bin_file}">Click here to download {file_label}</a>'

if __name__ == "__main__":
    main()
