import streamlit as st
from streamlit_option_menu import option_menu

# Import your pages here
import home, add_site, sites, jcb_work, add_ledger, ledger

st.set_page_config(page_title="Bansari Developers", page_icon="🏭")

# ----- CONFIGURATION -----
MENU = ["Home", "Add Site", "Manage Sites", "Manage JCB", "Add Ledger", "Manage Ledgers"]

# ----- INITIALIZE SESSION STATE -----
if "sidebar_open" not in st.session_state:
    st.session_state.sidebar_open = False
if "selected" not in st.session_state:
    st.session_state.selected = MENU[0]

# ----- CALLBACK FUNCTIONS -----
def open_sidebar():
    st.session_state.sidebar_open = True

def close_sidebar():
    st.session_state.sidebar_open = False

def select_menu(option):
    # Select the menu item and auto-collapse
    st.session_state.selected = option
    st.session_state.sidebar_open = False

# ----- LAYOUT WIDTHS -----
if st.session_state.sidebar_open:
    left_w, right_w = 0.22, 0.78
else:
    left_w, right_w = 0.06, 0.94

left_col, main_col = st.columns([left_w, right_w])

# ----- CUSTOM SIDEBAR -----
with left_col:
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    if st.session_state.sidebar_open:
        # Collapse button
        st.button("◀", key="collapse_btn", on_click=close_sidebar)

        st.markdown("### Navigation")
        # Menu as buttons (single-click behavior)
        for opt in MENU:
            st.button(opt, key=f"menu_{opt}", on_click=select_menu, args=(opt,))

    else:
        # Hamburger button to open sidebar
        st.button("☰", key="hamburger", on_click=open_sidebar)

# ----- MAIN CONTENT -----
with main_col:
    #st.title(f"🏗️ {st.session_state.selected}")
    if st.session_state.selected == "Home":
        home.page()
    elif st.session_state.selected == "Add Site":
        add_site.page1()
    elif st.session_state.selected == "Manage Sites":
        sites.page2()
    elif st.session_state.selected == "Manage JCB":
        jcb_work.page3()
    elif st.session_state.selected == "Add Ledger":
        add_ledger.page4()
    elif st.session_state.selected == "Manage Ledgers":
        ledger.page5()
    else:
        st.warning("Select Page Above")
