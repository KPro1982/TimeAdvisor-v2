
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

def GetFolderList(root=None):
    if(root == None):
       root = os.path.expanduser('~')
    subfolderObject = [x for x in os.scandir(root) ] 
    subfolders = [n.name for n in subfolderObject if n.is_dir() == True]
    cwd = os.getcwd()
    print(cwd)
    print("Subfolders(",cwd, ")", subfolders)
    return subfolders

def Config():
    subfolders = GetFolderList()
    source_folder = st.selectbox("Select Source Folder", options=subfolders)

configTab, reviewTab, submitTab = st.tabs(["Config", "Review", "Submit"])


with configTab:
 Config()


 