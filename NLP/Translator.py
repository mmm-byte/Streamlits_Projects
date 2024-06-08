import streamlit as st
import pandas as pd
from googletrans import Translator
import base64
from io import BytesIO

# Function to detect language
def detect_language(text):
    translator = Translator()
    return translator.detect(text).lang

# Function to translate text
def translate_text(text, dest_lang, src_lang):
    translator = Translator()
    return translator.translate(text, dest=dest_lang, src=src_lang).text


def translate_file(file, dest_lang, src_lang):
    translated_file = None
    if file.name.endswith('.xlsx'):
        df = pd.read_excel(file)
        df = df.applymap(lambda x: translate_text(str(x), dest_lang, src_lang))
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
        translated_file = output.getvalue()
    elif file.name.endswith('.txt'):
        text = file.getvalue().decode('utf-8')
        translated_text = translate_text(text, dest_lang, src_lang)
        translated_file = translated_text.encode('utf-8')
    return translated_file, file.name[:-4] + '_translated.xlsx'  # Change the file extension for Excel files


def main():
    st.title("Language Translator")

    # Input options
    input_type = st.radio("Select input type:", ("Text", "Upload File"))

    # Get user input
    if input_type == "Text":
        # Your existing text translation code here
        pass

    elif input_type == "Upload File":
        file = st.file_uploader("Upload a file:", type=['xlsx', 'txt'])
        if file is not None:
            src_lang = st.selectbox("Select input language:", ["Auto", "English", "French", "Spanish", "Chinese", "Japanese"])  # Add more languages as needed
            dest_lang = st.selectbox("Select output language:", ["English", "French", "Spanish", "Chinese", "Japanese"])  # Add more languages as needed
            if st.button("Translate"):
                if src_lang == "Auto":
                    text = file.getvalue().decode('utf-8')
                    src_lang = detect_language(text)
                translated_file, filename = translate_file(file, dest_lang.lower(), src_lang.lower())
                st.download_button(label="Download Translated File", data=translated_file, file_name=filename, mime="application/octet-stream")

if __name__ == "__main__":
    main()
