import streamlit as st
from streamlit_gsheets import GSheetsConnection
from pandas import DataFrame
from gspread_pandas import Spread,Client
from google.oauth2 import service_account

# Application Related Module
import pubchempy as pcp
from pysmiles import read_smiles
# 
import networkx as nx
import matplotlib.pyplot as plt

from datetime import datetime

url = "https://docs.google.com/spreadsheets/d/1JDy9md2VZPz4JbYtRPJLs81_3jUK47nx6GYQjgU8qNY/edit?usp=sharing"

# Check the connection
st.write(url)

sh = client.open(spreadsheetname)
worksheet_list = sh.worksheets()

# Functions 
@st.cache()
# Get our worksheet names
def worksheet_names():
    sheet_names = []   
    for sheet in worksheet_list:
        sheet_names.append(sheet.title)  
    return sheet_names

# Get the sheet as dataframe
def load_the_spreadsheet(spreadsheetname):
    worksheet = sh.worksheet(spreadsheetname)
    df = DataFrame(worksheet.get_all_records())
    return df

# Update to Sheet
def update_the_spreadsheet(spreadsheetname,dataframe):
    col = ['Compound CID','Time_stamp']
    spread.df_to_sheet(dataframe[col],sheet = spreadsheetname,index = False)
    st.sidebar.info('Updated to GoogleSheet')


st.header('Streamlit Chemical Inventory')

# Check whether the sheets exists
what_sheets = worksheet_names()
#st.sidebar.write(what_sheets)
ws_choice = st.sidebar.radio('Available worksheets',what_sheets)

# Load data from worksheets
df = load_the_spreadsheet(ws_choice)
# Show the availibility as selection
select_CID = st.sidebar.selectbox('CID',list(df['Compound CID']))

# Now we can use the pubchempy module to dump information
comp = pcp.Compound.from_cid(select_CID)
comp_dict = comp.to_dict() # Converting to a dictinoary
# What Information look for ?
options = ['molecular_weight' ,'molecular_formula',
           'charge','atoms','elements','bonds']
show_me = st.radio('What you want to see?',options)

st.info(comp_dict[show_me])
name = comp_dict['iupac_name']
st.markdown(name)
plot = st.checkbox('Canonical Smiles Plot')

if plot:
    sm = comp_dict['canonical_smiles']
    mol = read_smiles(comp_dict['canonical_smiles']) 
    elements = nx.get_node_attributes(mol, name = "element")
    nx.draw(mol, with_labels=True, labels = elements, pos=nx.spring_layout(mol))
    fig , ax = plt.subplots()
    nx.draw(mol, with_labels=True, labels = elements, pos = nx.spring_layout(mol))
    st.pyplot(fig)

add = st.sidebar.checkbox('Add CID')
if add :  
    cid_entry = st.sidebar.text_input('New CID')
    confirm_input = st.sidebar.button('Confirm')
    
    if confirm_input:
        now = datetime.now()
        opt = {'Compound CID': [cid_entry],
              'Time_stamp' :  [now]} 
        opt_df = DataFrame(opt)
        df = load_the_spreadsheet('Pending CID')
        new_df = df.append(opt_df,ignore_index=True)
        update_the_spreadsheet('Pending CID',new_df)
