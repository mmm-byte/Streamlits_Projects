import streamlit as st
import google.generativeai as genai

#Secret value
api_credentials = st.secrets[my_api_key]
st.write(api_credentials)
#Title
st.title('Welcome to SIF Feedback Chatbot')

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

genai.configure(api_key="api_credentials")
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
