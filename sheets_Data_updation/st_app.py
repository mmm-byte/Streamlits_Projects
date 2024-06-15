import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

url = 'https://docs.google.com/spreadsheets/d/178sSyO5YpLNOVz8XtZJTif6Vc07-K7Nncjp56TB3qb8/edit?usp=sharing'

conn = st.experimental_connection("gsheets", type=GSheetsConnection)

# Read data from the Google Sheet
df = conn.read(spreadsheet=url, usecols=[0, 1])
st.dataframe(df)

# Input field for user to add new data
new_data = st.text_input("Enter new data")

# Submit button to add new data to the Google Sheet
if st.button("Submit"):
    if new_data:
        # Append the new data to the DataFrame
        new_row = pd.DataFrame({df.columns[0]: [new_data], df.columns[1]: [""]})
        df = pd.concat([df, new_row], ignore_index=True)
        
        # Update the Google Sheet with the new data
        conn.update(spreadsheet=url, dataframe=df)
        st.success("Data added successfully!")
    else:
        st.error("Please enter some data.")
