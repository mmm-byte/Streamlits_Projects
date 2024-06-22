import streamlit as st
import google.generativeai as genai

#Secret value
api_credentials = st.secrets['my_api_key']
#st.write(api_credentials)

#Title
st.title('Welcome to SIF Feedback Chatbot')

def chat_message_with_buttons(role, content, options):
    st.chat_message(role).write(content)
    selected_option = None
    
    cols = st.columns(len(options))
    for i, option in enumerate(options):
        if cols[i].button(option):
            selected_option = option
    
    return selected_option

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Welcome to SIF Feedback Chtabot! May I know your Name"}]

options = ["Red", "Blue", "Green", "Yellow"]

for msg in st.session_state.messages:
    selected_option = chat_message_with_buttons(msg["role"], msg["content"], options)

genai.configure(api_key=api_credentials)
# for m in genai.list_models():
#   if 'generateContent' in m.supported_generation_methods:
#     print(m.name)
model = genai.GenerativeModel('gemini-1.5-flash')
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response =model.generate_content(prompt,stream=True)
    resp=''
    for chunk in response:
        resp=resp+chunk.text
    st.session_state.messages.append({"role": "assistant", "content": resp})
    st.chat_message("assistant").write(resp)
