
import streamlit as st
import os
import csv
import datetime
import pandas as pd
import time
import ctypes
import streamlit.components.v1 as components
import pandas as pd
import base64
import json

from ctypes import wintypes
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

if 'root_path'  not in st.session_state:
    st.session_state.root_path = os.getcwd()
if 'selected_folder'  not in st.session_state:
    st.session_state.selected_folder = os.getcwd()



# load the openai_api key
# openai_api_key = st.secrets["openai_api_key"]

def GetDesktopFolder():
    CSIDL_DESKTOP = 0
    _SHGetFolderPath = ctypes.windll.shell32.SHGetFolderPathW
    _SHGetFolderPath.argtypes = [wintypes.HWND,
                                ctypes.c_int,
                                wintypes.HANDLE,
                                wintypes.DWORD, wintypes.LPCWSTR]

    path_buf = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
    result = _SHGetFolderPath(0, CSIDL_DESKTOP, 0, 0, path_buf)
    return path_buf.value


def GetFolderList(root=None):
    if(root == None):
       root = os.path.expanduser('G:/Data/')
    subfolderObject = [x for x in os.scandir(root) ] 
    subfolders = [n.name for n in subfolderObject if n.is_dir() == True]
    cwd = os.getcwd()
    print(cwd)
    print("Subfolders(",cwd, ")", subfolders)
    return subfolders


@st.dialog("Select Folder")
def folder_selector():
    root_path = st.session_state.root_path
    selected_folder = st.session_state.selected_folder
    subfolderObject = [x for x in os.scandir(root_path) ] 
    subfolders = [n.name for n in subfolderObject if n.is_dir() == True]
    subfolders.insert(0,"Parent")
    subfolders.insert(0,"Desktop")


    st.text_input("Root Folder", value=root_path)
    selected_index = 0
    pos = 0
    for x in subfolders:
        if(st.button(x)):
            selected_index = pos
            if(selected_index == 0): # desktop
                st.session_state.root_path = GetDesktopFolder()
                st.session_state.selected_folder = ""
                subfolders.clear()
            elif(selected_index == 1): # parent
                st.session_state.root_path = Path(root_path).parent.absolute()
                st.session_state.selected_folder = ""
                subfolders.clear()
            else:
                if(st.session_state.selected_folder == subfolders[selected_index]):
                    st.session_state.root_path = os.path.join(root_path, selected_folder)
                    st.session_state.selected_folder = ""
                    subfolders.clear()
                else:
                    st.session_state.selected_folder = subfolders[selected_index]
            st.rerun(scope="fragment")  
        pos += 1
    button_label = "Select " + os.path.join(root_path, selected_folder)
    if(st.button(button_label, key="selectbutton", type="primary")):
        st.session_state.selected_path =  os.path.join(root_path, selected_folder)
        st.rerun()
        
      
    


def Config():
    
    if(st.button("Select Source Folder", key="SELECTFOLDER")):
        folder_selector()
    if 'selected_path' in st.session_state:
        st.write("Source folder = ", st.session_state.selected_path)

    uploaded_file = st.file_uploader("Select Client Data File")
    if uploaded_file:
        st.session_state.client_data_file = uploaded_file


def download_button(object_to_download, download_filename):
    """
    Generates a link to download the given object_to_download.
    Params:
    ------
    object_to_download:  The object to be downloaded.
    download_filename (str): filename and extension of file. e.g. mydata.csv,
    Returns:
    -------
    (str): the anchor tag to download object_to_download
    """
    if isinstance(object_to_download, pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False)

    # Try JSON encode for everything else
    else:
        object_to_download = json.dumps(object_to_download)

    try:
        # some strings <-> bytes conversions necessary here
        b64 = base64.b64encode(object_to_download.encode()).decode()

    except AttributeError as e:
        b64 = base64.b64encode(object_to_download).decode()

    dl_link = f"""
    <html>
    <head>
    <title>Start Auto Download file</title>
    <script src="http://code.jquery.com/jquery-3.2.1.min.js"></script>
    <script>
    $('<a href="data:text/csv;base64,{b64}" download="{download_filename}">')[0].click()
    </script>
    </head>
    </html>
    """
    return dl_link


def download_df():
    df = pd.DataFrame(st.session_state.col_values, columns=[st.session_state.col_name])
    components.html(
        download_button(df, st.session_state.filename),
        height=0,
    )


with st.form("my_form", clear_on_submit=False):
    st.text_input("Column name", help="Name of column", key="col_name")
    st.multiselect(
        "Entries", options=["A", "B", "C"], help="Entries in column", key="col_values"
    )
    st.text_input("Filename (must include .csv)", key="filename")
    submit = st.form_submit_button("Download dataframe", on_click=download_df)        


configTab, reviewTab, submitTab = st.tabs(["Config", "Review", "Submit"])


with configTab:
 Config()



 