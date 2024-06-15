import streamlit as st

from streamlit_gsheets import GSheetsConnection

url = 'https://docs.google.com/spreadsheets/d/178sSyO5YpLNOVz8XtZJTif6Vc07-K7Nncjp56TB3qb8/edit?usp=sharing'

conn = st.experimental_connection("gsheets", type=GSheetsConnection)

df = conn.read(spreadsheet=url, usecols=[0, 1])
st.dataframe(df)
