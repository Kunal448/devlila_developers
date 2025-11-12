import pandas as pd
import streamlit as st # type: ignore
from streamlit_gsheets import GSheetsConnection # type: ignore
from datetime import datetime
from fpdf import FPDF
import base64

def page3():
    def get_base64_of_image(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
            return base64.b64encode(data).decode()

    # Encode the image
    background_image_base64 = get_base64_of_image("jcb.jpg")
    
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
    
    st.markdown(page_bg_css, unsafe_allow_html=True)
    st.title("🚜 JCB Work")
    st.write("Manage your JCB income and payments here!")
    
    url = "https://docs.google.com/spreadsheets/d/1C0ogbuVVdgQtNmfiGGDI_3w6PxQaaojnFwbXJPo5nSQ/edit?usp=sharing"
    '''conn = st.connection("gsheets2", type = GSheetsConnection)
    
    data = conn.read(worksheet="Sheet1", ttl=0)
    df = pd.DataFrame(data)'''
    st.write("")
    st.write("")
    
    
    def new_data():
        conn = st.connection("gsheets2", type = GSheetsConnection, ttl = 60)
        if st.button("🔄 Refresh Data"):
            st.cache_data.clear()
            st.success("✅ Data refreshed!")
            st.rerun()
    
        data = conn.read(worksheet="Sheet1")
        df = pd.DataFrame(data)
        
        st.title("JCB Work New Entry")
            
        if df.iloc[0:1, 0:1].empty:
            maximum_srno = 0
            
        else:        
            maximum_srno = df.iloc[0:, 0:1].max()
            
            
        if df.iloc[3:4, 3:4].empty:
            maximum_chno = 0
            
        else:        
            maximum_chno = df.iloc[0:, 3:4].max()
        
        jcbw_sr_no, jcbw_date = st.columns([1,1])
        with jcbw_sr_no:
            j_sr_no1 = st.text_input("Serial Number", int(maximum_srno+1))
            jcbw_sr_no_int = int(j_sr_no1)
        with jcbw_date:
            l_date1 = st.date_input(
                "Select a date",
                None)
            jcbw_date_str = str(l_date1)
            
            
        jcbw_name, jcbw_ch_no = st.columns([2,1])
        with jcbw_name:
            j_name1 = st.text_input("Name", str(), placeholder="Enter Name")
            jcbw_name_str = str(j_name1)
        with jcbw_ch_no:
            j_ch_no1 = st.text_input("Challan Number", int(maximum_chno+1001))
            jcbw_ch_no_int = int(j_ch_no1)
            
        
        def mins(jcbw_time_str):
            hours, minutes = jcbw_time_str.split(':')
            total_minutes = int(hours) * 60 + int(minutes)
            return total_minutes
        
        jcbw_time, jcbw_rate = st.columns([1,1])
        with jcbw_time:
            j_time1 = st.text_input("Time", str("00:00"), placeholder="HH:MM")
            jcbw_time_str = str(j_time1)
        with jcbw_rate:
            j_rate1 = st.text_input("Rate", float())
            jcbw_rate_int = float(j_rate1)    
            
            
        jcbw_amount, jcbw_amount_received, jcbw_amount_pending = st.columns([1,1,1])
        with jcbw_amount:
            j_amount1 = st.text_input("Amount", int(mins(jcbw_time_str) * jcbw_rate_int))
            jcbw_amount_int = int(j_amount1)
        with jcbw_amount_received:
            j_amount_received1 = st.text_input("Amount Received", int())
            jcbw_amount_received_int = int(j_amount_received1)
        with jcbw_amount_pending:
            j_amount_pending1 = st.text_input("Amount Pending", int(jcbw_amount_int - jcbw_amount_received_int))
            jcbw_amount_pending_int = int(j_amount_pending1)  
            
            
        
        jcbw_contact, jcbw_remarks = st.columns([1,1])
        with jcbw_contact:
            j_contact1 = st.text_input("Contact No", int(), placeholder="Enter Contact Number")
            jcbw_contact_int = int(j_contact1)  
        with jcbw_remarks:
            j_remarks1 = st.text_area("Remarks", str(), placeholder="Enter any remarks here...")
            jcbw_remarks_str = str(j_remarks1) 
            
        
        if st.button("Submit", type="primary"):
            data = conn.read(worksheet="Sheet1", ttl=0)
            df = pd.DataFrame(data)
            
            #conn.read(worksheet="Sheet4", usecols=list(range(10)), ttl=2)
            existing_data = df
            existing_data = existing_data.dropna(how="all")
            
            result_data = pd.DataFrame(
                [
                    {
                        'SrNo': jcbw_sr_no_int,
                        'Date': jcbw_date_str,
                        'Name': jcbw_name_str,
                        'Ch_No': jcbw_ch_no_int,
                        'Time': jcbw_time_str,
                        'Rate': jcbw_rate_int,
                        'Amount': jcbw_amount_int,
                        'Amount_Received': jcbw_amount_received_int,
                        'Amount_Pending': jcbw_amount_pending_int,
                        'Contact_No': jcbw_contact_int,
                        'Remarks': jcbw_remarks_str
                    }
                ]
            )                
            updated_df = pd.concat([existing_data, result_data], ignore_index=True)            
            conn.update(worksheet="Sheet1", data=updated_df)                
            st.success("New JCB Work Data Saved Successfully")
            
            
    def view_data():
        conn = st.connection("gsheets2", type = GSheetsConnection, ttl=300)
        if st.button("🔄 Refresh Data", type="primary"):
            st.cache_data.clear()
            st.success("✅ Data refreshed!")
            st.rerun()
    
        data = conn.read(worksheet="Sheet1")
        df = pd.DataFrame(data)
        
        menu_select = st.selectbox("Select View", ['Select', 'All', 'Name Wise', 'Month Wise'])
        if menu_select == 'Select':
            pass
        
        elif menu_select == 'All':
            st.write("### All JCB Work Data")
            if df.empty:
                st.warning("No JCB Work Data Available")
            else:
                st.dataframe(df, hide_index=True)
            
        elif menu_select == 'Name Wise':
            name_list = df['Name'].unique().tolist()
            name_list.sort()
            name_list.insert(0, 'Select')
            name_select = st.selectbox("Select Name", name_list)
            if name_select == 'Select':
                pass
            else:
                filtered_df = df[df['Name'] == name_select]
                st.write(f"### JCB Work Data for {name_select}")
                filtered_df2 = pd.DataFrame(filtered_df)
                filtered_df2 = filtered_df.drop(["SrNo", "Name", "Rate", "Contact_No", "Remarks"], axis=1)
                filtered_df2['Ch_No'] = filtered_df['Ch_No'].astype(int)
                filtered_df2['Time'] = filtered_df['Time'].astype(str)
                filtered_df2['Amount'] = filtered_df['Amount'].astype(int)
                filtered_df2['Amount_Received'] = filtered_df['Amount_Received'].astype(int)
                filtered_df2['Amount_Pending'] = filtered_df['Amount_Pending'].astype(int)
                st.dataframe(filtered_df, hide_index=True)
                
                
                
                st.write("Total Amount: ", filtered_df2['Amount'].sum())
                st.write("Total Amount Received: ", filtered_df2['Amount_Received'].sum())
                st.write("Total Amount Pending: ", filtered_df2['Amount_Pending'].sum())
                
                
                class PDF(FPDF):
                    def header(self):
                        # Company logo
                        self.image("construction.png", 40, 8, 25)  # (x, y, width)
                        self.set_font("Times", "B", 25)
                        self.cell(0, 10, "Bansari Developers", ln=True, align="C")
                        self.ln(10)

                    def footer(self):
                        self.set_y(-15)
                        self.set_font("Helvetica", "I", 8)
                        self.cell(0, 10, f"Page {self.page_no()}", align="C")

                # ✅ Initialize PDF
                pdf = PDF()
                pdf.set_auto_page_break(auto=True, margin=15)
                pdf.add_page()
                pdf.set_font("Helvetica", size=10)
                
                pdf.set_font("Helvetica", "B", 12)
                pdf.cell(17, 10, "Ledger: ", ln = False, align="L")
                pdf.set_font("Helvetica", "", 12)
                pdf.cell(20, 10, f"{name_select}") 
                pdf.ln(10)
                
                filtered_df["Date"] = pd.to_datetime(filtered_df["Date"])
                filtered_df = filtered_df.sort_values(by="Date")
                from_date = filtered_df["Date"].iloc[0].strftime("%d-%m-%Y")
                to_date = filtered_df["Date"].iloc[-1].strftime("%d-%m-%Y")
                pdf.set_font("Helvetica", "B", 12)
                pdf.cell(16, 10, f"Period: ", align="L")
                pdf.set_font("Helvetica", "", 12)
                pdf.cell(30, 10, f"From {from_date} To {to_date}", align="L")
                pdf.ln(10)
                
                pdf.set_font("Helvetica", "BU", 12)        
                pdf.cell(0, 10, "JCB Ledger Report", align="C")
                pdf.ln(10)

                # ✅ Add Table Header
                col_width = 32 # auto-fit
                row_height = 8
                
                pdf.set_font("Helvetica", "B", 10)
                for col in filtered_df2.columns:
                    pdf.cell(col_width, row_height, col, align="C")
                pdf.ln(row_height)
                
                total_cols = ['Amount', 'Amount_Received', 'Amount_Pending']

                # Calculate totals
                total_amount = filtered_df2['Amount'].sum()
                total_amount_received = filtered_df2['Amount_Received'].sum()
                total_amount_pending = filtered_df2['Amount_Pending'].sum()

                # Create total row
                total_row = {}
                for col in filtered_df2.columns:
                    if col == 'Amount':
                        total_row[col] = total_amount
                    elif col == 'Amount_Received':
                        total_row[col] = total_amount_received
                    elif col == 'Amount_Pending':
                        total_row[col] = total_amount_pending
                    else:
                        total_row[col] = ''

                # Label for total row
                total_row['Date'] = 'Total'

                # Append total row to dataframe
                df_final = pd.concat([filtered_df2, pd.DataFrame([total_row])], ignore_index=True)

                '''# ✅ Add Table Rows
                pdf.set_font("Helvetica", "", 10)
                for i in range(len(df_final)):
                    for col in df_final.columns:
                        text = str(df_final.iloc[i][col])
                        pdf.cell(col_width, row_height, text, align="C")
                    pdf.ln(row_height)'''
        
                for i in range(len(df_final)):
                    row = df_final.iloc[i]
                    # ✅ Check if this is the total row
                    if str(row["Date"]).lower() == "total":
                        pdf.cell(0, 0, "-"*160, align="C", ln=True)
                        pdf.set_font("Helvetica", "B", 10)
                        
                    else:
                        pdf.set_font("Helvetica", "", 10)

                    for col in df_final.columns:
                        pdf.cell(col_width, row_height, str(row[col]), align="C")
                    pdf.ln(row_height)
                pdf.set_font("Helvetica", "", 10)    
                pdf.cell(0, 0, "-"*160, align="C", ln=True)
                st.write("")   
                st.write("")
            
                var = 0
                if st.button("Generate JCB Ledger Report"):
                    pdf.output(f"JCB_Ledger_Report_{name_select}.pdf")
                    var = 1
                    
                    st.success("Report Generated Successfully")
                if var == 1:
                    with open(f"JCB_Ledger_Report_{name_select}.pdf", "rb") as f:
                        st.download_button("Download PDF", f, f"JCB_Ledger_Report_{name_select}.pdf")
                
        elif menu_select == 'Month Wise':
            month_list = df['Date'].apply(lambda x: x[:7]).unique().tolist()
            month_list.sort()
            month_list.insert(0, 'Select')
            month_select = st.selectbox("Select Month", month_list)
            if month_select == 'Select':
                pass
            else:
                filtered_df = df[df['Date'].apply(lambda x: x[:7]) == month_select]
                st.write(f"### JCB Work Data for {month_select}")
                df_sorted = filtered_df.sort_values(by='Date', ascending=True)
                st.dataframe(df_sorted, hide_index=True)
                        
        else:
            st.write("Select a valid view")
            
            
            
    def update_data():
        conn = st.connection("gsheets2", type = GSheetsConnection, ttl=60)
        
        if st.button("🔄 Refresh Data"):
            st.cache_data.clear()
            st.success("✅ Data refreshed!")
            st.rerun()
    
        data = conn.read(worksheet="Sheet1")
        df = pd.DataFrame(data)
        
        st.title("Update JCB Work Data")
        
        jcbw_ch_no, _ = st.columns([1,1])
        with jcbw_ch_no:
            j_ch_no2 = st.text_input("Enter Challan No: ", int(1001))
            jcbw_ch_no_int = int(j_ch_no2)
            
        row = df[df['Ch_No'] == jcbw_ch_no_int].iloc[0]
        st.subheader("Enter JCB Work Details")
        
        jcbw_sr_no, jcbw_date = st.columns([1,1])
        with jcbw_sr_no:
            j_sr_no1 = st.text_input("Serial Number", int(row['SrNo']))
            jcbw_sr_no_int = int(j_sr_no1)
        with jcbw_date:
            l_date1 = st.text_input(
                "Select a date",
                str(row['Date']))
            jcbw_date_str = str(l_date1)
            
            
        jcbw_name, jcbw_ch_no = st.columns([2,1])
        with jcbw_name:
            j_name1 = st.text_input("Name", row['Name'], placeholder="Enter Name")
            jcbw_name_str = str(j_name1)
        with jcbw_ch_no:
            j_ch_no1 = st.text_input("Challan Number", int(row['Ch_No']))
            jcbw_ch_no_int = int(j_ch_no1)
            
        
        def mins(jcbw_time_str):
            hours, minutes = jcbw_time_str.split(':')
            total_minutes = int(hours) * 60 + int(minutes)
            return total_minutes
        
        jcbw_time, jcbw_rate = st.columns([1,1])
        with jcbw_time:
            j_time1 = st.text_input("Time", row['Time'], placeholder="HH:MM")
            jcbw_time_str = str(j_time1)
        with jcbw_rate:
            j_rate1 = st.text_input("Rate", int(row['Rate']))
            jcbw_rate_int = int(j_rate1)    
            
            
        jcbw_amount, jcbw_amount_received, jcbw_amount_pending = st.columns([1,1,1])
        with jcbw_amount:
            j_amount1 = st.text_input("Amount", int(row['Amount']))
            jcbw_amount_int = int(j_amount1)
        with jcbw_amount_received:
            j_amount_received1 = st.text_input("Amount Received", int(row['Amount_Received']))
            jcbw_amount_received_int = int(j_amount_received1)
        with jcbw_amount_pending:
            j_amount_pending1 = st.text_input("Amount Pending", int(jcbw_amount_int - jcbw_amount_received_int))
            jcbw_amount_pending_int = int(j_amount_pending1)  
            
            
        
        jcbw_contact, jcbw_remarks_str = st.columns([1,1])
        with jcbw_contact:
            j_contact1 = st.text_input("Contact No", int(row['Contact_No']), placeholder="Enter Contact Number")
            jcbw_contact_int = int(j_contact1)
        with jcbw_remarks_str:
            j_remarks1 = st.text_area("Remarks", str(row['Remarks']), placeholder="Enter any remarks here...")
            jcbw_remarks_str = str(j_remarks1)
            
            
        if st.button("Update"):
            condition = df['SrNo'] == jcbw_sr_no_int
        
            result_data = {
                    'SrNo': jcbw_sr_no_int,
                    'Date': jcbw_date_str,
                    'Name': jcbw_name_str,
                    'Ch_No': jcbw_ch_no_int,
                    'Time': jcbw_time_str,
                    'Rate': jcbw_rate_int,
                    'Amount': jcbw_amount_int,
                    'Amount_Received': jcbw_amount_received_int,
                    'Amount_Pending': jcbw_amount_pending_int,
                    'Contact_No': jcbw_contact_int,
                    'Remarks': jcbw_remarks_str
                }
            
            df.loc[condition, list(result_data.keys())] = list(result_data.values())
            conn.update(worksheet="Sheet1", data=df)
            
            st.success("JCB Work Data Successfully Updated")
            
            
    def delete_data():
        conn = st.connection("gsheets2", type = GSheetsConnection, ttl=60)
        
        if st.button("🔄 Refresh Data"):
            st.cache_data.clear()
            st.success("✅ Data refreshed!")
            st.rerun()
    
        data = conn.read(worksheet="Sheet1")
        df = pd.DataFrame(data)
        
        st.title("Delete JCB Work Data")
        
        jcbw_ch_no, _ = st.columns([1,1])
        with jcbw_ch_no:
            j_ch_no2 = st.text_input("Enter Challan No: ", int(1001))
            jcbw_ch_no_int = int(j_ch_no2)
            
        row = df[df['Ch_No'] == jcbw_ch_no_int].iloc[0]
        st.subheader("JCB Work Details")
        
        st.write(f"**SrNo:**{'&nbsp;'*60} {int(row['SrNo'])}")
        st.write(f"**Date:**{'&nbsp;'*60} {row['Date']}")
        st.write(f"**Name:**{'&nbsp;'*57} {row['Name']}")
        st.write(f"**Challan No:**{'&nbsp;'*46} {int(row['Ch_No'])}")
        st.write(f"**Time:**{'&nbsp;'*58} {row['Time']}")
        st.write(f"**Rate:**{'&nbsp;'*59} {int(row['Rate'])}")
        st.write(f"**Amount:**{'&nbsp;'*52} {int(row['Amount'])}")
        st.write(f"**Amount Received:**{'&nbsp;'*32} {int(row['Amount_Received'])}")
        st.write(f"**Amount Pending:**{'&nbsp;'*34} {int(row['Amount_Pending'])}")
        st.write(f"**Contact No:**{'&nbsp;'*47} {int(row['Contact_No'])}")
        st.write(f"**Remarks:**{'&nbsp;'*52} {str(row['Remarks'])}")
            
        if st.button("Delete"):
            condition = df['Ch_No'] == jcbw_ch_no_int
            df = df[~condition]
            conn.update(worksheet="Sheet1", data=df)
            st.success("JCB Work Data Successfully Deleted")
        
        
        
    
    
    def select_work():
        work_select = st.selectbox("Choose Task: ", ['Select', 'New Data', 'View Data', 'Update Data', 'Delete Data'])
        if work_select == 'Select':
            pass
        elif work_select == 'New Data':
            new_data()
        elif work_select == 'View Data':
            view_data()
        elif work_select == 'Update Data':
            update_data()   
        elif work_select == 'Delete Data':
            delete_data()
        else:
            st.write("Select a valid task")
            
    select_work()
