import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import numpy as np

def page1():
    st.title("🏗️ Add New Site Page")
    st.write("Add a new construction site!")
    
    url = "https://docs.google.com/spreadsheets/d/1OliyAKJqz_A2NNVcRBdEpkqnUrnGOLaWsAD1niC9F9U/edit?usp=sharing"
    conn = st.connection("gsheets", type = GSheetsConnection)
    
    data = conn.read(worksheet="Sheet1", ttl=2)
    df = pd.DataFrame(data)
    max_site = df['Sheet'].max()  
    if np.isnan(max_site):
        max_site = 0
    st.write(f"Current number of sites: {'&nbsp;'*1} {int(max_site)}")
    st.write("")
    st.write("")
    site, _ = st.columns([1, 1])
    with site:
        site1 = st.text_input("Site Name", str(), placeholder="Type site name here...")
        site_str = str(site1)
        
    save_site = st.button("Add Site", type="primary")
        
    if save_site:
        existing_data = conn.read(worksheet="Sheet1", usecols=list(range(2)), ttl=2)
        existing_data = existing_data.dropna(how="all")            
        result_data = pd.DataFrame(
            [
                {
                    "Sheet": max_site + 1,
                    "Sites": site_str
                }
            ]
        )        
        updated_df = pd.concat([existing_data, result_data], ignore_index=True)    
        conn.update(worksheet="Sheet1", data=updated_df)        
        st.success("New Site Saved Successfully")