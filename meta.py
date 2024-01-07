# define meta information of the app
import streamlit as st



def meta():
    
    st.set_page_config(page_icon="⚗️", page_title="Omnigpt", layout="centered") # or layout='centered'
    # page_bg_img = '''
    #     <style>
    #     body {
    #     background-image: url("https://images.unsplash.com/photo-1452179535021-368bb0edc3a8?q=80&w=2048&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
    #     background-size: cover;
    #     }
    #     </style>
    #     '''

    # st.markdown(page_bg_img, unsafe_allow_html=True)
    st.image('RS5537_Metabolic_7pillars_EnglishTitles_v05_CB.png')
    st.write("# 🌲 Ask the Sustainability AI Expert for Professional Evaluation")

    

    # Hide the made with Streamlit footer
    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    # Hide the specific class of deploy and connect to streamlit.io
    st.markdown(
        """
        <style>
            .st-emotion-cache-zq5wmm.ezrtsby0 {
                display: none !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
