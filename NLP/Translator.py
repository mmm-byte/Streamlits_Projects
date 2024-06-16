import streamlit as st
from transformers import M2M100ForConditionalGeneration, M2M100Tokenizer

# Load the model and tokenizer
model_name = "facebook/m2m100_418M"
tokenizer = M2M100Tokenizer.from_pretrained(model_name)
model = M2M100ForConditionalGeneration.from_pretrained(model_name)

# Streamlit app
st.title("Language Translation with M2M100")

# User input
source_text = st.text_area("Enter text to translate:")
source_lang = st.text_input("Enter source language code (e.g., en for English):")
target_lang = st.text_input("Enter target language code (e.g., hi for Hindi):")

# Translation
if st.button("Translate"):
    if source_text and source_lang and target_lang:
        tokenizer.src_lang = source_lang
        encoded_text = tokenizer(source_text, return_tensors="pt")
        generated_tokens = model.generate(**encoded_text, forced_bos_token_id=tokenizer.get_lang_id(target_lang))
        translated_text = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
        st.write("Translated text:")
        st.write(translated_text)
    else:
        st.write("Please provide text and language codes for translation.")
