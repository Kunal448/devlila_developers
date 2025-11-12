import pandas as pd
import streamlit as st # type: ignore
from streamlit_gsheets import GSheetsConnection # type: ignore
from datetime import date
import base64



# Main Function

def page2():
    def get_base64_of_image(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
            return base64.b64encode(data).decode()

    # Encode the image
    background_image_base64 = get_base64_of_image("construction.png")
    
    # Inject CSS
    page_bg_css = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/png;base64,{background_image_base64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    [data-testid="stAppViewContainer"]::before {{
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0, 0.85); /* White overlay with 60% opacity */
        z-index: 0;
    }}
    </style>
    """
    
    st.markdown(page_bg_css, unsafe_allow_html=True)
    st.title("🏗️ Manage Sites")
    st.write("Manage all your currently active sites here!")
    st.write("")
    st.write("")
    
    url = "https://docs.google.com/spreadsheets/d/1OliyAKJqz_A2NNVcRBdEpkqnUrnGOLaWsAD1niC9F9U/edit?usp=sharing"
    conn = st.connection("gsheets", type = GSheetsConnection, ttl=60)
    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.success("✅ Data refreshed!")
        st.rerun()
    
    data = conn.read(worksheet="Sheet1")
    df = pd.DataFrame(data)       
        
    
    
    
    
    
    # Function to Add New Data
    
    def new_data(sheet_num):
        conn = st.connection("gsheets", type = GSheetsConnection, ttl=60)
        if st.button("🔄 Refresh Data "):
            st.cache_data.clear()
            st.success("✅ Data refreshed!")
            st.rerun()
        
        '''data1 = conn.read(worksheet="Sheet2", ttl=2)
        df1 = pd.DataFrame(data1)'''
    
        data = conn.read(worksheet=sheet_num+1)
        df = pd.DataFrame(data)
        
        st.title(f'You are in {site_select}')
        
        table_select = st.selectbox("Select Table", ['Select', 'Labour', 'JCB', 'Materials', 'Cement', 'Other Vehicles', 'Other Expenses'])
        if table_select == 'Select':
            pass
        elif table_select == 'Labour':
            st.title("Labour New Entry")
            
            if df.iloc[0:1, 1:2].empty:
                maximum_labour = 0
                
            else:        
                maximum_labour = df.iloc[0:, 1:2].max()
            
            labour_sr_no, labour_date = st.columns([1,1])
            with labour_sr_no:
                l_sr_no1 = st.text_input("Serial Number", int(maximum_labour+1))
                labour_sr_no_int = int(l_sr_no1)
            with labour_date:
                l_date1 = st.date_input("Date", None)
                labour_date_str = str(l_date1)
                
            labour_person, labour_rate = st.columns([1,1])
            with labour_person:
                l_person1 = st.text_input("No. of Persons", int())
                labour_person_int = int(l_person1)
            #df1.loc[df["Work"] == "Labour", "Rate"].values[0]
            with labour_rate:
                l_rate1 = st.text_input("Labour Rate", int())
                labour_rate_int = int(l_rate1)
                
            labour_amount, _ = st.columns([1,1])
            with labour_amount:
                l_amount1 = st.text_input("Labour Amount: ", int(labour_person_int * labour_rate_int))
                labour_amount_int = int(l_amount1)
                
            add_labour_data = st.button("Add Labour Data")
            if add_labour_data:
                
                data = conn.read(worksheet=sheet_num+1, ttl=0)
                df = pd.DataFrame(data)
                
                #conn.read(worksheet="Sheet4", usecols=list(range(10)), ttl=2)
                existing_data = df
                existing_data = existing_data.dropna(how="all")
                
                result_data = pd.DataFrame(
                    [
                        {
                            "SrNo": labour_sr_no_int,
                            "Date": labour_date_str,
                            "Work": "Labour",
                            "Persons": labour_person_int,
                            "Type": "",
                            "Time": "",
                            "Weight/Bags": "",
                            "Rate": labour_rate_int,
                            "Particular": "",
                            "Amount": labour_amount_int
                        }
                    ]
                )                
                updated_df = pd.concat([existing_data, result_data], ignore_index=True)            
                conn.update(worksheet=sheet_num+1, data=updated_df)                
                st.success("New Labour Data Saved Successfully")
                
                
        elif table_select == 'JCB':
            st.title("JCB New Entry")
            if df.iloc[0:1, 1:2].empty:
                maximum_jcb = 0
                
            else:        
                maximum_jcb = df.iloc[0:, 1:2].max()
            
            jcb_sr_no, jcb_date = st.columns([1,1])
            with jcb_sr_no:
                j_sr_no1 = st.text_input("Serial Number", int(maximum_jcb+1))
                jcb_sr_no_int = int(j_sr_no1)
            with jcb_date:
                j_date1 = st.date_input("Date", None)
                jcb_date_str = str(j_date1)
                
            jcb_time, jcb_rate = st.columns([1,1])
            with jcb_time:
                j_time1 = st.text_input("Time in Hours", int())
                jcb_time_int = int(j_time1)
            with jcb_rate:
                j_rate1 = st.text_input("JCB Rate per Hour", int())
                jcb_rate_int = int(j_rate1)
                
            jcb_amount, _ = st.columns([1,1])
            with jcb_amount:
                j_amount1 = st.text_input("JCB Amount", int(jcb_time_int * jcb_rate_int))
                jcb_amount_int = int(j_amount1)
                
                
            add_jcb_data = st.button("Add JCB Data")
            if add_jcb_data:
                
                data = conn.read(worksheet=sheet_num+1, ttl=0)
                df = pd.DataFrame(data)
                
                #conn.read(worksheet="Sheet4", usecols=list(range(10)), ttl=2)
                existing_data = df
                existing_data = existing_data.dropna(how="all")
                
                result_data = pd.DataFrame(
                    [
                        {
                            "SrNo": jcb_sr_no_int,
                            "Date": jcb_date_str,
                            "Work": "JCB",
                            "Persons": "",
                            "Type": "",
                            "Time": jcb_time_int,
                            "Weight/Bags": "",
                            "Rate": jcb_rate_int,
                            "Particular": "",
                            "Amount": jcb_amount_int
                        }
                    ]
                )                
                updated_df = pd.concat([existing_data, result_data], ignore_index=True)            
                conn.update(worksheet=sheet_num+1, data=updated_df)                
                st.success("New JCB Data Saved Successfully")
        
        
        elif table_select == 'Materials':
            st.title("Materials New Entry")
            if df.iloc[0:1, 1:2].empty:
                maximum_materials = 0
                
            else:        
                maximum_materials = df.iloc[0:, 1:2].max()
            
            materials_sr_no, materials_date = st.columns([1,1])
            with materials_sr_no:
                m_sr_no1 = st.text_input("Serial Number", int(maximum_materials+1))
                materials_sr_no_int = int(m_sr_no1)
            with materials_date:
                m_date1 = st.date_input("Date", None)
                materials_date_str = str(m_date1)
                
            materials_type, materials_weight = st.columns([1,1])
            with materials_type:
                m_type1 = st.selectbox("Type of Material", ['Select', 'GSB', 'WMM', 'Sand', 'Kapchi', 'Steel', 'Brick', 'Moram', 'Black Soil', 'RCC Pipe', 'PVC Pipe'])      
                materials_type_str = str(m_type1)
                
            if materials_type_str == 'Brick' or materials_type_str == 'RCC Pipe' or materials_type_str == 'PVC Pipe':
                with materials_weight:
                    m_weight1 = st.text_input("No. of Pieces", float())
                    materials_weight_int = float(m_weight1)
                
                materials_rate, materials_amount = st.columns([1,2])
                with materials_rate:
                    m_rate1 = st.text_input("Rate per Piece", float())
                    materials_rate_int = float(m_rate1)   
                with materials_amount:
                    m_amount1 = st.text_input("Materials Amount", float(materials_weight_int * materials_rate_int))
                    materials_amount_int = float(m_amount1)
            else:
                with materials_weight:
                    m_weight1 = st.text_input("Weight in tons", float())
                    materials_weight_int = float(m_weight1)
                
                materials_rate, materials_amount = st.columns([1,2])
                with materials_rate:
                    m_rate1 = st.text_input("Rate per ton", float())
                    materials_rate_int = float(m_rate1)   
                with materials_amount:
                    m_amount1 = st.text_input("Materials Amount", float(materials_weight_int * materials_rate_int))
                    materials_amount_int = float(m_amount1)
                
                
            add_materials_data = st.button("Add Materials Data")
            if add_materials_data:
                
                data = conn.read(worksheet=sheet_num+1, ttl=0)
                df = pd.DataFrame(data)
                
                #conn.read(worksheet="Sheet4", usecols=list(range(10)), ttl=2)
                existing_data = df
                existing_data = existing_data.dropna(how="all")
                
                result_data = pd.DataFrame(
                    [
                        {
                            "SrNo": materials_sr_no_int,
                            "Date": materials_date_str,
                            "Work": "Materials",
                            "Persons": "",
                            "Type": materials_type_str,
                            "Time": "",
                            "Weight/Bags": materials_weight_int,
                            "Rate": materials_rate_int,
                            "Particular": "",
                            "Amount": materials_amount_int
                        }
                    ]
                )                
                updated_df = pd.concat([existing_data, result_data], ignore_index=True)            
                conn.update(worksheet=sheet_num+1, data=updated_df)                
                st.success("New Materials Data Saved Successfully")
                
                
        elif table_select == 'Cement':
            st.title("Cement New Entry")
            if df.iloc[0:1, 1:2].empty: 
                maximum_cement = 0
            else:        
                maximum_cement = df.iloc[0:, 1:2].max()
            
            cement_sr_no, cement_date = st.columns([1,1])
            with cement_sr_no:
                c_sr_no1 = st.text_input("Serial Number", int(maximum_cement+1))
                cement_sr_no_int = int(c_sr_no1)
            with cement_date:
                c_date1 = st.date_input("Date", None)
                cement_date_str = str(c_date1)
                
            
            cement_type, cement_bags = st.columns([1,1])
            with cement_type:
                c_type1 = st.selectbox("Type of Cement", ['Select', 'OPC', 'PPC'])      
                cement_type_str = str(c_type1)
            with cement_bags:
                c_bags1 = st.text_input("No. of Bags", int())
                cement_bags_int = int(c_bags1)
                
            cement_rate, cement_amount = st.columns([1,2])
            with cement_rate:   
                c_rate1 = st.text_input("Rate per Bag", int())
                cement_rate_int = int(c_rate1)
            with cement_amount:
                c_amount1 = st.text_input("Cement Amount", int(cement_bags_int * cement_rate_int))
                cement_amount_int = int(c_amount1)
                
                
            add_cement_data = st.button("Add Cement Data")
            if add_cement_data:
                
                data = conn.read(worksheet=sheet_num+1, ttl=0)
                df = pd.DataFrame(data)
                
                #conn.read(worksheet="Sheet4", usecols=list(range(10)), ttl=2)
                existing_data = df
                existing_data = existing_data.dropna(how="all")
                
                result_data = pd.DataFrame(
                    [
                        {
                            "SrNo": cement_sr_no_int,
                            "Date": cement_date_str,
                            "Work": "Cement",
                            "Persons": "",
                            "Type": cement_type_str,
                            "Time": "",
                            "Weight/Bags": cement_bags_int,
                            "Rate": cement_rate_int,
                            "Particular": "",
                            "Amount": cement_amount_int
                        }
                    ]
                )                
                updated_df = pd.concat([existing_data, result_data], ignore_index=True)            
                conn.update(worksheet=sheet_num+1, data=updated_df)                
                st.success("New Cement Data Saved Successfully")
                
                
        
        elif table_select == 'Other Vehicles':
            st.title("Other Vehicles New Entry")
            if df.iloc[0:1, 1:2].empty: 
                maximum_vehicles = 0
            else:        
                maximum_vehicles = df.iloc[0:, 1:2].max()
                
            vehicles_sr_no, vehicles_date = st.columns([1,1])
            with vehicles_sr_no:
                v_sr_no1 = st.text_input("Serial Number", int(maximum_vehicles+1))
                vehicles_sr_no_int = int(v_sr_no1)
            with vehicles_date:
                v_date1 = st.date_input("Date", None)
                vehicles_date_str = str(v_date1)
                
            vehicles_type, vehicles_time = st.columns([1,1])
            with vehicles_type:
                v_type1 = st.selectbox("Type of Vehicle", ['Select', 'Truck', 'Bulldozer', 'Crane', 'Forklift', 'Roller', 'Tractor'])
                vehicles_type_str = str(v_type1)
            with vehicles_time:
                v_time1 = st.text_input("Vehicle Time", int())
                vehicles_time_int = int(v_time1)
                
            vehicles_rate, vehicles_amount = st.columns([1,2])
            with vehicles_rate:
                v_rate1 = st.text_input("Rate per Hour", int())
                vehicles_rate_int = int(v_rate1)
            with vehicles_amount:
                v_amount1 = st.text_input("Vehicle Amount", int(vehicles_time_int * vehicles_rate_int))
                vehicles_amount_int = int(v_amount1)
                
                
            add_vehicles_data = st.button("Add Other Vehicles Data")
            if add_vehicles_data:
                
                data = conn.read(worksheet=sheet_num+1, ttl=0)
                df = pd.DataFrame(data)
                
                #conn.read(worksheet="Sheet4", usecols=list(range(10)), ttl=2)
                existing_data = df
                existing_data = existing_data.dropna(how="all")
                
                result_data = pd.DataFrame(
                    [
                        {
                            "SrNo": vehicles_sr_no_int,
                            "Date": vehicles_date_str,
                            "Work": "Other Vehicles",
                            "Persons": "",
                            "Type": vehicles_type_str,
                            "Time": vehicles_time_int,
                            "Weight/Bags": "",
                            "Rate": vehicles_rate_int,
                            "Particular": "",
                            "Amount": vehicles_amount_int
                        }
                    ]
                )                
                updated_df = pd.concat([existing_data, result_data], ignore_index=True)            
                conn.update(worksheet=sheet_num+1, data=updated_df)                
                st.success("New Other Vehicles Data Saved Successfully")
                
                
                
        elif table_select == 'Other Expenses':
            st.title("Other Expenses New Entry")
            if df.iloc[0:1, 1:2].empty: 
                maximum_expenses = 0
            else:        
                maximum_expenses = df.iloc[0:, 1:2].max()
                
            expenses_sr_no, expenses_date = st.columns([1,1])
            with expenses_sr_no:
                e_sr_no1 = st.text_input("Serial Number", int(maximum_expenses+1))
                expenses_sr_no_int = int(e_sr_no1)
            with expenses_date:
                e_date1 = st.date_input("Date", None)
                expenses_date_str = str(e_date1)
                
            expenses_particular, expenses_amount = st.columns([2,1])
            with expenses_particular:
                e_particular1 = st.text_area("Particulars", str(), placeholder="Type particulars here...")
                expenses_particular_str = str(e_particular1)
            with expenses_amount:
                e_amount1 = st.text_input("Expense Amount", int())
                expenses_amount_int = int(e_amount1)
                
                
            add_expenses_data = st.button("Add Other Expenses Data")
            if add_expenses_data:
                
                data = conn.read(worksheet=sheet_num+1, ttl=0)
                df = pd.DataFrame(data)
                
                #conn.read(worksheet="Sheet4", usecols=list(range(10)), ttl=2)
                existing_data = df
                existing_data = existing_data.dropna(how="all")
                
                result_data = pd.DataFrame(
                    [
                        {
                            "SrNo": expenses_sr_no_int,
                            "Date": expenses_date_str,
                            "Work": "Other Expenses",
                            "Persons": "",
                            "Type": "",
                            "Time": "",
                            "Weight/Bags": "",
                            "Rate": "",
                            "Particular": expenses_particular_str,
                            "Amount": expenses_amount_int
                        }
                    ]
                )                
                updated_df = pd.concat([existing_data, result_data], ignore_index=True)            
                conn.update(worksheet=sheet_num+1, data=updated_df)                
                st.success("New Other Expenses Data Saved Successfully")
                
                
        else:
            st.write("Select a valid table")
                
                
                
                
                
                
                
                
                
                
                
                
    def view_data(sheet_num):
        conn = st.connection("gsheets", type = GSheetsConnection, ttl=60)
        
        if st.button("🔄 Refresh Data "):
            st.cache_data.clear()
            st.success("✅ Data refreshed!")
            st.rerun()
    
        data = conn.read(worksheet=sheet_num+1)
        df = pd.DataFrame(data)
        
        st.title(f'You are in {site_select}')
        
        table_select = st.selectbox("Select Table", ['Select', 'Labour', 'JCB', 'Materials', 'Cement', 'Other Vehicles', 'Other Expenses'])
        if table_select == 'Select':
            pass
        
        elif table_select == 'Labour':
            st.title("Labour Data")
            labour_data = df.loc[df['Work'] == 'Labour']
            df_clean = labour_data.dropna(axis=1, how='all')
            if df_clean.empty:
                st.warning("No Labour Data Available")
            else:
                st.dataframe(df_clean)
                total_labour = labour_data['Amount'].sum()
                st.write(f'Total Labour Amount: {total_labour} Rs')
            
            
        elif table_select == 'JCB':
            st.title("JCB Data")
            jcb_data = df.loc[df['Work'] == 'JCB']
            df_clean = jcb_data.dropna(axis=1, how='all')
            if df_clean.empty:
                st.warning("No JCB Data Available")
            else:
                st.dataframe(df_clean)
                total_jcb = jcb_data['Amount'].sum()
                st.write(f'Total JCB Amount: {total_jcb} Rs')
            
            
        elif table_select == 'Materials':
            st.title("Materials Data")
            materials_data = df.loc[df['Work'] == 'Materials']
            df_clean = materials_data.dropna(axis=1, how='all')
            if df_clean.empty:
                st.warning("No Materials Data Available")
            else:
                st.dataframe(df_clean)
                total_materials = materials_data['Amount'].sum()
                st.write(f'Total Materials Amount: {total_materials} Rs')
            
            
        elif table_select == 'Cement':
            st.title("Cement Data")
            cement_data = df.loc[df['Work'] == 'Cement']
            df_clean = cement_data.dropna(axis=1, how='all')
            if df_clean.empty:
                st.warning("No Cement Data Available")
            else:
                st.dataframe(df_clean)
                total_cement = cement_data['Amount'].sum()
                st.write(f'Total Cement Amount: {total_cement} Rs')
            
        
        elif table_select == 'Other Vehicles':
            st.title("Other Vehicles Data")
            vehicles_data = df.loc[df['Work'] == 'Other Vehicles']
            df_clean = vehicles_data.dropna(axis=1, how='all')
            if df_clean.empty:
                st.warning("No Other Vehicles Data Available")
            else:
                st.dataframe(df_clean)
                total_vehicles = vehicles_data['Amount'].sum()
                st.write(f'Total Other Vehicles Amount: {total_vehicles} Rs')
            
            
        elif table_select == 'Other Expenses':
            st.title("Other Expenses Data")
            expenses_data = df.loc[df['Work'] == 'Other Expenses']
            df_clean = expenses_data.dropna(axis=1, how='all')
            if df_clean.empty:
                st.warning("No Other Expenses Data Available")
            else:
                st.dataframe(df_clean)
                total_expenses = expenses_data['Amount'].sum()
                st.write(f'Total Other Expenses Amount: {total_expenses} Rs')
            
            
        else:
            st.write("Select a valid table")
                
                

        
        
    
    
    
    # Function to Open Worksheet Based on Site Selection
    
    def open_worksheet(site_sheet_num):
        work_select = st.selectbox("Choose Task: ", ['Select', 'New Data', 'View Data', 'Update Data', 'Delete Data'])
        if work_select == 'Select':
            pass
        elif work_select == 'New Data':
            new_data(site_sheet_num)
        elif work_select == 'View Data':
            view_data(site_sheet_num)
        elif work_select == 'Update Data':
            pass    
        elif work_select == 'Delete Data':
            pass
        else:
            st.write("Select a valid task")
        
     
    l = df['Sites'].tolist()
    if len(l) == 0:
        st.warning("No Sites Available. Please add new site first.")
        
    else:
        site_select = st.selectbox("Select Site", l)    
        result = df.loc[df['Sites'] == site_select.strip(), 'Sheet']     
        
        # Main Call to Open Worksheet            
        open_worksheet(int(result.iloc[0]))   
