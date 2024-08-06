
import streamlit as st
import os
import csv
import datetime
import pandas as pd
import time

from enum import Enum
from os import listdir
from os.path import join, isfile
from datetime import datetime
from pathlib import Path
from dataclasses import astuple, dataclass, field

st.set_page_config(
    page_title="TimeAdvisor", 
    page_icon=None, 
    layout="wide", 
    menu_items=None
    )



if 'entryIndex' not in st.session_state:
    st.session_state.entryIndex = 0

if 'timeEntries' not in st.session_state:
    st.session_state.timeEntries = []


# load the openai_api key
openai_api_key = st.secrets["OpenAI_key"]

def GetFolderList():
   cwd = os.getcwd()
   subfolders = os.walk(cwd)
   print(cwd, subfolders)

def Config():
    source_folder = st.selectbox("Select Source Folder")
    GetFolderList()

configTab, reviewTab, submitTab = st.tabs(["Config", "Review", "Submit"])


with configTab:
 Config()


 