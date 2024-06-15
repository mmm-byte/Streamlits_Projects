import streamlit as st

# Define the questions for each language
questions = {
    "en": ["What is your name?", "This training is relevant to my needs and/or interests?", "I have learnt new skills and/or knowledge through this training?"],
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
    # Print the responses
    st.write("Responses:")
    for question, response in zip(questions[selected_lang_code], responses):
        st.write(f"{question}: {response}")
