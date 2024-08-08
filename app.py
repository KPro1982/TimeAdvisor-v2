
import streamlit as st
import csv
import datetime
import pandas as pd
import time
import pandas as pd
import dataclasses

from dataclasses import astuple, dataclass, field

st.set_page_config(
    page_title="TimeAdvisor", 
    page_icon=None, 
    layout="wide", 
    menu_items=None
    )




# load the openai_api key
# openai_api_key = st.secrets["openai_api_key"]

    
    


def Config():
    
    uploaded_file = st.file_uploader("Select Client Data File", accept_multiple_files=True)
    if uploaded_file:
        st.session_state.client_data_file = uploaded_file




configTab, reviewTab, submitTab = st.tabs(["Config", "Review", "Submit"])


with configTab:
 Config()



 