
import streamlit as st
import os
import csv
import datetime
import pandas as pd
import time
import ctypes

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


        


configTab, reviewTab, submitTab = st.tabs(["Config", "Review", "Submit"])


with configTab:
 Config()


 