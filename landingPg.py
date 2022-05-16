import cv2
from pages.pg1 import newSession
from pages.pg2 import continueSession
import streamlit as st
import time



placeholder = st.empty()
userImg = None
with placeholder.container():
    st.text("landing page")

    page = st.radio("Start A Fresh Session",("Yep", "Nope"))
    
    time.sleep(1)
placeholder.empty()

if page == "Yep": 
    with placeholder.container():
                
        st.title("Webcam Application")
        run = st.checkbox('Run',value = True)
        FRAME_WINDOW = st.image([])
        cam = cv2.VideoCapture(0)
        
        while run:
            ret, frame = cam.read()
            try:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            except:
                continue
            cv2.imwrite('data/setupImg.jpg',frame) 
            FRAME_WINDOW.image(frame)
               
        else:            
            st.write('Photo Taken')
            placeholder.empty()       
    continueSession()
else :
    placeholder.empty()    
    continueSession()

