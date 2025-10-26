import pandas as pd
import streamlit as st # type: ignore
from streamlit_gsheets import GSheetsConnection # type: ignore
import base64
import numpy as np 

def page4():
    conn = st.connection("gsheets3", type = GSheetsConnection)
    data = conn.read(worksheet="Sheet1", ttl=0)
    st.title("🏗️ Ledger Companies")
    st.write("Add New Ledger Company Name!")  
    df = pd.DataFrame(data)
    max_ledger = df['Sheet'].max()  
    if np.isnan(max_ledger):
        max_ledger = 0
    st.write(f"Current number of Ledgers: {'&nbsp;'*1} {int(max_ledger)}")
    st.write("")
    st.write("")
    if df.iloc[0:1, 1:2].empty:
        maximum_ledger = 0
        
    else:        
        maximum_ledger = df.iloc[0:, 0:1].max()
        
    company, _ = st.columns([1, 1])
    with company:
        company1 = st.text_input("Company Name", str(), placeholder="Type company name here...")
        company_str = str(company1)
        
    if st.button("Add Company", type="primary"):
        existing_data = conn.read(worksheet="Sheet1", usecols=list(range(2)), ttl=0)
        existing_data = existing_data.dropna(how="all")            
        result_data = pd.DataFrame(
            [
                {
                    "Sheet": int(maximum_ledger) + 1,
                    "Company": company_str
                }
            ]
        )        
        updated_df = pd.concat([existing_data, result_data], ignore_index=True)    
        conn.update(worksheet="Sheet1", data=updated_df)        
        st.success("New Company Saved Successfully")