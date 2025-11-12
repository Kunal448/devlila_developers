import pandas as pd
import streamlit as st # type: ignore
from streamlit_gsheets import GSheetsConnection # type: ignore
from datetime import datetime
import base64

VEHICLES = ["Camper", "Tractor", "JCB"]
EXPENSES = ["Diesel", "EMI", "Repair", "Other"]

def page6():
    '''def get_base64_of_image(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
            return base64.b64encode(data).decode()

    # Encode the image
    background_image_base64 = get_base64_of_image("ledger.jpg")
    
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
        background: rgba(0,0,0, 0.88); /* White overlay with 60% opacity */
        z-index: 0;
    }}
    </style>
    """
    
    st.markdown(page_bg_css, unsafe_allow_html=True)'''
    st.title("🛑 Vehicle Expenses💨")
    st.write("View all your vehicle expenses here.")
    
    st.write("")
    st.write("")
    conn = st.connection("gsheets4", type = GSheetsConnection, ttl=60)
    if st.button("🔄 Refresh Data "):
        st.cache_data.clear()
        st.success("✅ Data refreshed!")
        st.rerun()
        
    @st.cache_data(ttl=60)
    def get_data():
        data = conn.read(worksheet="Sheet1")
        return pd.DataFrame(data)
    
    def new_data():
        df = get_data()
        
        st.subheader("➕ Add New Vehicle Expense")
            
        if df.iloc[0:1, 0:1].empty:
            maximum_srno = 0
            
        else:        
            maximum_srno = df.iloc[0:, 0:1].max()
        
        ve_sr_no, ve_date = st.columns([1,1])
        with ve_sr_no:
            v_sr_no1 = st.text_input("Serial Number", int(maximum_srno+1))
            ve_sr_no_int = int(v_sr_no1)
        with ve_date:
            v_date1 = st.date_input(
                "Select a date",
                None)
            ve_date_str = str(v_date1)
            
            
        ve_vehicle, ve_expense = st.columns([1,1])
        with ve_vehicle:
            v_vehicle1 = st.selectbox("Vehicle", ["Select"] + VEHICLES)
            ve_vehicle_str = str(v_vehicle1)
        with ve_expense:
            v_expense1 = st.selectbox("Expense", ["Select"] + EXPENSES)
            ve_expense_str = str(v_expense1)
            
            
        
        ve_amount, ve_remarks = st.columns([1,1])
        with ve_amount:
            v_amount1 = st.text_input("Amount", int(),  placeholder="Enter Amount")
            ve_amount_int = int(v_amount1)  
        with ve_remarks:
            v_remarks1 = st.text_area("Remarks", str(), placeholder="Enter any remarks here...")
            ve_remarks_str = str(v_remarks1) 
            
        
        if st.button("Submit", type="primary"):
            existing_data = df
            existing_data = existing_data.dropna(how="all")
            
            result_data = pd.DataFrame(
                [
                    {
                        'SrNo': ve_sr_no_int,
                        'Date': ve_date_str,
                        'Vehicle': ve_vehicle_str,
                        'Expense': ve_expense_str,
                        'Amount': ve_amount_int,
                        'Remarks': ve_remarks_str
                    }
                ]
            )                
            updated_df = pd.concat([existing_data, result_data], ignore_index=True)            
            conn.update(worksheet="Sheet1", data=updated_df)                
            st.success("✅ New Vehicle Expense Data Saved Successfully")
            st.cache_data.clear()
            st.rerun()
    
    
    def view_data():
        df = get_data()
        
        st.subheader("👀 View Vehicle Expenses")
        menu_select = st.selectbox("Select View", ['Select', 'All', 'Vehicle Wise', 'Month Wise', 'Vehicle & Month Wise'])
        st.write("")
        st.write("")
        if menu_select == 'Select':
            pass
        
        elif menu_select == 'All':
            st.write("### All Vehicle Expense Data")
            st.dataframe(df, hide_index=True)
                
        elif menu_select == 'Vehicle Wise':
            vehicle_choice = st.selectbox("Select Vehicle", ['Select', 'Camper', 'Tractor', 'JCB'])
            if vehicle_choice == 'Select':
                pass
            else:
                st.write(f"### Vehicle Expense Data for {vehicle_choice}")
                filtered_df = df[df['Vehicle'] == vehicle_choice]
                st.dataframe(filtered_df, hide_index=True)
                st.write(f"Total Amount: {'&nbsp;'*1} ₹ {sum(filtered_df['Amount'].astype(int))}")
                
                
        elif menu_select == 'Month Wise':
            month_list = df['Date'].apply(lambda x: x[:7]).unique().tolist()
            month_list.sort()
            month_list.insert(0, 'Select')
            month_select = st.selectbox("Select Month", month_list)
            if month_select == 'Select':
                pass
            else:
                filtered_df = df[df['Date'].apply(lambda x: x[:7]) == month_select]
                st.write(f"### Vehicle Expense Data for {month_select}")
                df_sorted = filtered_df.sort_values(by='Date', ascending=True)
                st.dataframe(df_sorted, hide_index=True)
                st.write(f"Total Amount: {'&nbsp;'*1} ₹ {sum(filtered_df['Amount'].astype(int))}")
                
                
                
        elif menu_select == 'Vehicle & Month Wise':
            vehicle_choice = st.selectbox("Select Vehicle", ['Select', 'Camper', 'Tractor', 'JCB'])
            month_list = df['Date'].apply(lambda x: x[:7]).unique().tolist()
            month_list.sort()
            month_list.insert(0, 'Select')
            month_select = st.selectbox("Select Month", month_list)
            if vehicle_choice == 'Select' or month_select == 'Select':
                pass
            else:
                filtered_df = df[(df['Vehicle'] == vehicle_choice) & (df['Date'].apply(lambda x: x[:7]) == month_select)]
                st.write(f"### Vehicle Expense Data for {vehicle_choice} in {month_select}")
                df_sorted = filtered_df.sort_values(by='Date', ascending=True)
                st.dataframe(df_sorted, hide_index=True)
                st.write(f"Total Amount: {'&nbsp;'*1} ₹ {sum(filtered_df['Amount'].astype(int))}")
                
        else:
            st.write("Select a valid view")
    
    
    
    def update_data():
        df = get_data()
        
        st.subheader("✏️ Update Vehicle Expense Data")
        
        ve_sr_no, _ = st.columns([1,1])
        with ve_sr_no:
            ve_sr_no2 = st.text_input("Enter Sr No: ", int(), placeholder="Enter Serial Number to Update")
            ve_sr_no_int = int(ve_sr_no2)
            
        row = df[df['SrNo'] == ve_sr_no_int].iloc[0]
        st.subheader("Enter Vehicle Expense Details")
        
        
        ve_sr_no, ve_date = st.columns([1,1])
        with ve_sr_no:
            v_sr_no1 = st.text_input("Serial Number", int(row['SrNo']))
            ve_sr_no_int = int(v_sr_no1)
        with ve_date:
            v_date1 = st.text_input(
                "Select a date",
                str(row['Date']))
            ve_date_str = str(v_date1)
            
            
        ve_vehicle, ve_expense = st.columns([1,1])
        with ve_vehicle:
            v_vehicle1 = st.selectbox("Vehicle", VEHICLES, index=VEHICLES.index(row["Vehicle"]))
            ve_vehicle_str = str(v_vehicle1)
        with ve_expense:
            v_expense1 = st.selectbox("Expense", EXPENSES, index=EXPENSES.index(row["Expense"]))
            ve_expense_str = str(v_expense1)
            
            
        
        ve_amount, ve_remarks = st.columns([1,1])
        with ve_amount:
            v_amount1 = st.text_input("Amount", int(row['Amount']), placeholder="Enter Amount")
            ve_amount_int = int(v_amount1)  
        with ve_remarks:
            v_remarks1 = st.text_area("Remarks", str(row['Remarks']), placeholder="Enter any remarks here...")
            ve_remarks_str = str(v_remarks1)
    
        
        
        if st.button("Update", type="primary"):
            condition = df['SrNo'] == ve_sr_no_int
        
            result_data = {
                    'SrNo': ve_sr_no_int,
                    'Date': ve_date_str,
                    'Vehicle': ve_vehicle_str,
                    'Expense': ve_expense_str,
                    'Amount': ve_amount_int,
                    'Remarks': ve_remarks_str
                }
            
            df.loc[condition, list(result_data.keys())] = list(result_data.values())
            conn.update(worksheet="Sheet1", data=df)
            
            st.success("✅ Vehicle Expense Data Updated Successfully") 
            st.cache_data.clear()
            st.rerun()  
    
    def delete_data():
        df = get_data()
        
        st.subheader("🗑️ Delete Vehicle Expense Data")
        
        ve_sr_no, _ = st.columns([1,1])
        with ve_sr_no:
            ve_sr_no2 = st.text_input("Enter Sr No: ", int())
            ve_sr_no_int = int(ve_sr_no2)
            
        row = df[df['SrNo'] == ve_sr_no_int].iloc[0]
        st.subheader("Vehicle Expense Details")
        
        st.write(f"**SrNo:**{'&nbsp;'*50} {int(row['SrNo'])}")
        st.write(f"**Date:**{'&nbsp;'*51} {row['Date']}")
        st.write(f"**Vehicle:**{'&nbsp;'*45} {row['Vehicle']}")
        st.write(f"**Expense:**{'&nbsp;'*43} {row['Expense']}")
        st.write(f"**Amount:**{'&nbsp;'*44} {int(row['Amount'])}")
        st.write(f"**Remarks:**{'&nbsp;'*43} {row['Remarks']}")
            
        if st.button("Delete", type="primary"):
            condition = df['SrNo'] == ve_sr_no_int
            df = df[~condition]
            conn.update(worksheet="Sheet1", data=df)
            st.success("✅ Vehicle Expense Data Deleted Successfully")
            st.cache_data.clear()
            st.rerun()
    
    
    
    
    
    
    
    
    work_select = st.selectbox("Choose Task: ", ['Select', 'New Data', 'View Data', 'Update Data', 'Delete Data'])
    st.write("")
    st.write("")
    if work_select == 'New Data':
        new_data()
    elif work_select == 'View Data':
        view_data()
    elif work_select == 'Update Data':
        update_data()   
    elif work_select == 'Delete Data':
        delete_data()
    else:
        st.warning("Select a task")
    
