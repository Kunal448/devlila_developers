import streamlit as st
from streamlit_option_menu import option_menu

# Import your pages here
import home, add_site, sites, jcb_work, add_ledger, ledger, vehicle_expenses

st.set_page_config(page_title="Devlila Developers", page_icon="🏭", initial_sidebar_state="collapsed")



with st.sidebar:
    selected = option_menu(
        "Main Menu", ["Home", "Add Site", "Manage Sites", "Manage JCB", "Add Ledger", "Manage Ledgers", "Vehicle Expenses"],
        icons=[],
        menu_icon="cast", default_index=0,
        styles={
        }
    )

if selected == "Home":
    home.page()
elif selected == "Add Site":
    add_site.page1()
elif selected == "Manage Sites":
    sites.page2()
elif selected == "Manage JCB":
    jcb_work.page3()
elif selected == "Add Ledger":
    add_ledger.page4()
elif selected == "Manage Ledgers":
    ledger.page5()
elif selected == "Vehicle Expenses":
    vehicle_expenses.page6()
else:
    st.warning("Select Page Above")

