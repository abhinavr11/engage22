import cv2
from pages.pg1 import newSession
from pages.pg2 import continueSession
import streamlit as st
import time

placeholder = st.empty()


page1 = False
page2 = False
with placeholder.container():
    st.text("landing page")

    page = st.radio("Start A Fresh Session",("Yep", "Nope"))
    
    time.sleep(1)

if page == "Yep":
    placeholder.empty()
    st.markdown('<h1 style="background-color:green;">',unsafe_allow_html=True)
    st.text('Streamlit is **_really_ cool**.')
    st.markdown('</h1>',unsafe_allow_html=True)
    newSession()

else :
    placeholder.empty()
    
    continueSession()

