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
    translated_file_path = ""
    if file_path.endswith('.xlsx'):
        df = pd.read_excel(file_path)
        df = df.applymap(lambda x: translate_text(str(x), dest_lang, src_lang))
        translated_file_path = os.path.join("translated_files", "translated.xlsx")
        df.to_excel(translated_file_path, index=False)
    elif file_path.endswith('.pptx') or file_path.endswith('.docx') or file_path.endswith('.txt'):
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            translated_text = translate_text(text, dest_lang, src_lang)
        translated_file_path = os.path.join("translated_files", "translated.txt")
        with open(translated_file_path, 'w', encoding='utf-8') as file:
            file.write(translated_text)
    return translated_file_path

# Main function
def main():
    st.title("Language Translator")

    # Ensure translated files directory exists
    if not os.path.exists("translated_files"):
        os.makedirs("translated_files")

    # Input options
    input_type = st.radio("Select input type:", ("Text", "Upload File"))

    # Get user input
    if input_type == "Text":
        text = st.text_area("Enter text to translate:")
        src_lang = st.selectbox("Select input language:", ["Auto", "English", "Chinese", "Japanese", "Korean", "Indonesian"])  # Add more languages as needed
        dest_lang = st.selectbox("Select output language:", ["English", "Chinese", "Japanese", "Korean", "Indonesian"])  # Add more languages as needed
        if st.button("Translate"):
            if src_lang == "Auto":
                src_lang = detect_language(text)
            translated_text = translate_text(text, dest_lang.lower(), src_lang.lower())
            st.write("Translated Text:")
            st.write(translated_text)
            translated_file_path = os.path.join("translated_files", "translated_text.txt")
            with open(translated_file_path, 'w', encoding='utf-8') as file:
                file.write(translated_text)
            st.write(f"Translated text saved to {translated_file_path}")

    elif input_type == "Upload File":
        file = st.file_uploader("Upload a file:", type=['xlsx', 'pptx', 'docx', 'txt'])
        if file is not None:
            if not os.path.exists("temp"):
                os.makedirs("temp")
            file_path = os.path.join("temp", file.name)
            with open(file_path, 'wb') as f:
                f.write(file.getvalue())
            src_lang = st.selectbox("Select input language:", ["Auto", "English", "Chinese", "Japanese", "Korean", "Indonesian"])  # Add more languages as needed
            dest_lang = st.selectbox("Select output language:", ["English", "Chinese", "Japanese", "Korean", "Indonesian"])  # Add more languages as needed
            if st.button("Translate"):
                if src_lang == "Auto":
                    with open(file_path, 'r', encoding='utf-8') as f:
                        text = f.read()
                        src_lang = detect_language(text)
                translated_file_path = translate_file(file_path, dest_lang.lower(), src_lang.lower())
                st.write("File Translated Successfully!")
                st.write(f"Translated file saved to {translated_file_path}")

if __name__ == "__main__":
    main()
