import pandas as pd
import streamlit as st # type: ignore
from streamlit_gsheets import GSheetsConnection # type: ignore
from fpdf import FPDF # type: ignore
from datetime import date
import base64

def page5():
    def get_base64_of_image(file_path):
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
    
    st.markdown(page_bg_css, unsafe_allow_html=True)
    st.title("📒 Ledger Reports")
    st.write("View and download ledger reports.")
    
    st.write("")
    st.write("")
    conn = st.connection("gsheets3", type = GSheetsConnection, ttl=60)
    if st.button("🔄 Refresh Data "):
        st.cache_data.clear()
        st.success("✅ Data refreshed!")
        st.rerun()
    
    data = conn.read(worksheet="Sheet1")
    df = pd.DataFrame(data)       
    
    
    
    
    
    
    
    def new_data(sheet_num):
        st.title("Enter New Ledger Data")
        conn = st.connection("gsheets3", type = GSheetsConnection, ttl=60)
        
        if st.button("🔄 Refresh Data"):
            st.cache_data.clear()
            st.success("✅ Data refreshed!")
            st.rerun()
        data = conn.read(worksheet=f"Sheet{sheet_num+1}")
        df = pd.DataFrame(data)
        
        if df.iloc[0:1, 1:2].empty:
            maximum_srno = 0
            
        else:        
            maximum_srno = df.iloc[0:, 1:2].max()
            
        if df.iloc[0:1, 3:4].empty:
            maximum_bill_no = 1000
            
        else:        
            maximum_bill_no = df.iloc[0:, 3:4].max()
            
            
        ledger_sr_no, ledger_date = st.columns([1,1])
        with ledger_sr_no:
            l_sr_no1 = st.text_input("Serial Number", int(maximum_srno+1))
            ledger_sr_no_int = int(l_sr_no1)
        with ledger_date:
            l_date1 = st.date_input("Date", None)
            ledger_date_str = str(l_date1)
            

        ledger_bill_no, _ = st.columns([1,1])
        with ledger_bill_no:
            l_bill_no1 = st.text_input("Bill No", int(maximum_bill_no+1))
            ledger_bill_no_int = int(l_bill_no1)
            
            
        
        ledger_debit, ledger_credit = st.columns([1,1])
        with ledger_debit:
            l_debit1 = st.text_input("Debit Amount", int())
            ledger_debit_int = int(l_debit1)
        with ledger_credit:
            l_credit1 = st.text_input("Credit Amount", int())
            ledger_credit_int = int(l_credit1)
            
        if df.iloc[0:1, 6:7].empty:
            last_value = 0
        else:
            last_value = df["Balance"].iloc[-1]
        ledger_balance, ledger_remarks = st.columns([1,1])
        with ledger_balance:
            l_balance1 = st.text_input("Balance Amount", int(last_value + (ledger_debit_int - ledger_credit_int)))
            ledger_balance_int = int(l_balance1)
        with ledger_remarks:
            l_remarks1 = st.text_area("Remarks", str(), placeholder="Enter any remarks here...")
            ledger_remarks_str = str(l_remarks1)
        
        
        if st.button("Add Ledger Data", type="primary"):
                
            data = conn.read(worksheet=f"Sheet{sheet_num+1}", ttl=0)
            df = pd.DataFrame(data)
            existing_data = df
            existing_data = existing_data.dropna(how="all")
            
            result_data = pd.DataFrame(
                [
                    {
                        "SrNo": ledger_sr_no_int,
                        "Date": ledger_date_str,
                        "BillNo": ledger_bill_no_int,
                        "Debit_Amount": ledger_debit_int,
                        "Credit_Amount": ledger_credit_int,
                        "Balance": ledger_balance_int,
                        "Remarks": ledger_remarks_str
                    }
                ]
            )                
            updated_df = pd.concat([existing_data, result_data], ignore_index=True)            
            conn.update(worksheet=f"Sheet{sheet_num+1}", data=updated_df)                
            st.success("New Ledger Data Saved Successfully")
            
            
    def view_data(sheet_num):
        st.title("View Ledger Data")
        conn = st.connection("gsheets3", type = GSheetsConnection, ttl=300)
        if st.button("🔄 Refresh Data"):
            st.cache_data.clear()
            st.success("✅ Data refreshed!")
            st.rerun()
        data = conn.read(worksheet=f"Sheet{sheet_num+1}")
        df = pd.DataFrame(data)
        if df.empty:
            st.warning("No Ledger Data Available")
        else:
            df2 = pd.DataFrame(data)
            df1 = df.drop("Company Name", axis=1)
            df1['SrNo'] = df['SrNo'].astype(int)
            df1['BillNo'] = df['BillNo'].astype(int)
            df1['Debit_Amount'] = df['Debit_Amount'].astype(int)
            df1['Credit_Amount'] = df['Credit_Amount'].astype(int)
            df1['Balance'] = df['Balance'].astype(int)
            df1["Remarks"] = df["Remarks"].fillna("")
            
            df2 = df.drop("Company Name", axis=1)
            df2['SrNo'] = df['SrNo'].astype(int)
            df2['BillNo'] = df['BillNo'].astype(int)
            df2['Debit_Amount'] = df['Debit_Amount'].astype(int)
            df2['Credit_Amount'] = df['Credit_Amount'].astype(int)
            df2['Balance'] = df['Balance'].astype(int)
            df2["Remarks"] = df["Remarks"].fillna("")
            
            
            st.dataframe(df2, hide_index=True)
            st.write("Total Debit Amount: ", df2['Debit_Amount'].sum())
            st.write("Total Credit Amount: ", df2['Credit_Amount'].sum())
            st.write("Total Balance Amount Left: ", df2['Debit_Amount'].sum() - df2['Credit_Amount'].sum())
            
            
            class PDF(FPDF):
                def header(self):
                    # Company logo
                    self.image("construction.png", 40, 8, 25)  # (x, y, width)
                    self.set_font("Times", "B", 25)
                    self.cell(0, 10, "Devlila Developers", ln=True, align="C")
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
            pdf.cell(20, 10, f"{company_select}") 
            pdf.ln(10)
            
            df1["Date"] = pd.to_datetime(df1["Date"])
            df1 = df1.sort_values(by="Date")
            from_date = df1["Date"].iloc[0].strftime("%d-%m-%Y")
            to_date = df1["Date"].iloc[-1].strftime("%d-%m-%Y")
            pdf.set_font("Helvetica", "B", 12)
            pdf.cell(16, 10, f"Period: ", align="L")
            pdf.set_font("Helvetica", "", 12)
            pdf.cell(30, 10, f"From {from_date} To {to_date}", align="L")
            pdf.ln(10)
            
            pdf.set_font("Helvetica", "BU", 12)        
            pdf.cell(0, 10, "Account Ledger Report", align="C")
            pdf.ln(10)

            # ✅ Add Table Header
            col_width = pdf.w / (len(df1.columns) + 1)  # auto-fit
            row_height = 8
            
            pdf.set_font("Helvetica", "B", 10)
            for col in df1.columns:
                pdf.cell(col_width, row_height, col, align="C")
            pdf.ln(row_height)
            
            total_cols = ['Debit_Amount', 'Credit_Amount', 'Balance']

            # Calculate totals
            debit_total = df2['Debit_Amount'].sum()
            credit_total = df2['Credit_Amount'].sum()
            balance_total = debit_total - credit_total

            # Create total row
            total_row = {}
            for col in df2.columns:
                if col == 'Debit_Amount':
                    total_row[col] = debit_total
                elif col == 'Credit_Amount':
                    total_row[col] = credit_total
                elif col == 'Balance':
                    total_row[col] = balance_total
                else:
                    total_row[col] = ''

            # Label for total row
            total_row['Date'] = 'Total'

            # Append total row to dataframe
            df_final = pd.concat([df2, pd.DataFrame([total_row])], ignore_index=True)

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
            if st.button("Generate Ledger Report"):
                pdf.output(f"Ledger_Report_{company_select}.pdf")
                var = 1
                
                st.success("Report Generated Successfully")
            if var == 1:
                with open(f"Ledger_Report_{company_select}.pdf", "rb") as f:
                    st.download_button("Download PDF", f, f"Ledger_Report_{company_select}.pdf") 
            
            
            
            
    def delete_data(sheet_num):
        st.title("Delete Ledger Data")
        conn = st.connection("gsheets3", type = GSheetsConnection, ttl=60)
        if st.button("🔄 Refresh Data"):
            st.cache_data.clear()
            st.success("✅ Data refreshed!")
            st.rerun()
        data = conn.read(worksheet=f"Sheet{sheet_num+1}")
        df = pd.DataFrame(data)
        if df.empty:
            st.warning("No Ledger Data Available")
        else:
            df2 = df.drop("Company Name", axis=1)
            df2['SrNo'] = df['SrNo'].astype(int)
            df2['BillNo'] = df['BillNo'].astype(int)
            df2['Debit_Amount'] = df['Debit_Amount'].astype(int)
            df2['Credit_Amount'] = df['Credit_Amount'].astype(int)
            df2['Balance'] = df['Balance'].astype(int)
            df2["Remarks"] = df["Remarks"].fillna("")
            bill_no_del = st.text_input("Enter Bill Number to Delete Record: ", int(1001))
            bill_no_del_int = int(bill_no_del)
            
            row = df[df['BillNo'] == bill_no_del_int].iloc[0]
            st.subheader("Ledger Entry Details")
            
            st.write(f"**Sr No:**{'&nbsp;'*60} {int(row['SrNo'])}")
            st.write(f"**Date:**{'&nbsp;'*61} {row['Date']}")
            st.write(f"**Bill No:**{'&nbsp;'*57} {int(row['BillNo'])}")
            st.write(f"**Debit Amount:**{'&nbsp;'*42} {int(row['Debit_Amount'])}")
            st.write(f"**Credit Amount:**{'&nbsp;'*40} {int(row['Credit_Amount'])}")
            st.write(f"**Balance:**{'&nbsp;'*55} {int(row['Balance'])}")
            st.write(f"**Remarks:**{'&nbsp;'*53} {row['Remarks']}")
            if st.button("Delete Entry"):
                df = df[df['BillNo'] != bill_no_del_int]
                conn.update(worksheet=f"Sheet{sheet_num+1}", data=df)                
                st.success("Ledger Data Deleted Successfully")
    
    
    
    def open_worksheet(site_sheet_num):
        work_select = st.selectbox("Choose Task: ", ['Select', 'New Data', 'View Data', 'Delete Data'])
        if work_select == 'Select':
            pass
        elif work_select == 'New Data':
            new_data(site_sheet_num)
        elif work_select == 'View Data':
            view_data(site_sheet_num)  
        elif work_select == 'Delete Data':
            delete_data(site_sheet_num)
        else:
            st.write("Select a valid task")
        
    
    
    
    
    
    l = df['Company'].tolist() 
    if l==[]:
        st.warning("No Ledger Companies Available. Please add a company first.")
    else:
        company_select = st.selectbox("Select Company", l)    
        result = df.loc[df['Company'] == company_select.strip(), 'Sheet']

        open_worksheet(int(result.iloc[0]))
