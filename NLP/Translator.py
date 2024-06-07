import streamlit as st
from googletrans import Translator
import pandas as pd
import os
import base64

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
        return "translated.xlsx"
    elif file_path.endswith('.pptx') or file_path.endswith('.docx') or file_path.endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            translated_text = translate_text(text, dest_lang, src_lang)
        with open("translated.txt", 'w', encoding='utf-8') as file:
            file.write(translated_text)
        return "translated.txt"

# Main function
def main():
    st.title("Language Translator")

    # Input options
    input_type = st.radio("Select input type:", ("Text", "Upload File"))

    # Get user input
    if input_type == "Text":
        text = st.text_area("Enter text to translate:")
        src_lang = st.selectbox("Select input language:", ["Auto", "English", "Chinese", "Japanese", "Korean", "Indonesia"])  # Add more languages as needed
        dest_lang = st.selectbox("Select output language:", ["English", "Chinese", "Japanese", "Korean", "Indonesia"])  # Add more languages as needed
        if st.button("Translate"):
            if src_lang == "Auto":
                src_lang = detect_language(text)
            translated_text = translate_text(text, dest_lang.lower(), src_lang.lower())
            st.write("Translated Text:")
            st.write(translated_text)
            download_link = get_download_link(translated_text, "translated_text.txt")
            st.markdown(download_link, unsafe_allow_html=True)

    elif input_type == "Upload File":
        file = st.file_uploader("Upload a file:", type=['xlsx', 'pptx', 'docx', 'txt'])
        if file is not None:
            if not os.path.exists("temp"):
                os.makedirs("temp")
            file_path = os.path.join("temp", file.name)
            with open(file_path, 'wb') as f:
                f.write(file.getvalue())
            src_lang = st.selectbox("Select input language:", ["Auto", "English", "Chinese", "Japanese", "Korean", "Indonesia"])  # Add more languages as needed
            dest_lang = st.selectbox("Select output language:", ["English", "Chinese", "Japanese", "Korean", "Indonesia"])  # Add more languages as needed
            if st.button("Translate"):
                if src_lang == "Auto":
                    with open(file_path, 'r', encoding='utf-8') as f:
                        text = f.read()
                        src_lang = detect_language(text)
                translated_file = translate_file(file_path, dest_lang.lower(), src_lang.lower())
                st.write("File Translated Successfully!")
                download_link = get_download_link(translated_file, translated_file)
                st.markdown(download_link, unsafe_allow_html=True)

def get_download_link(file_content, file_name):
    b64 = base64.b64encode(file_content.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{file_name}">Click here to download {file_name}</a>'

if __name__ == "__main__":
    main()
