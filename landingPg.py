import cv2
from pages.pg1 import newSession
from pages.pg2 import continueSession
import streamlit as st
import time
import pymongo
import os


def cleanDatabase():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["masterdatabase"]
    dbs = ['Attention','Luminosity','Posture'] #removed BodyFat for now
    for db in dbs:
        mycol = mydb[db]

        mycol.drop()

        print(mydb.list_collection_names())   

def cleanImgs():
    if os.path.isfile("D:\Engage\streamlit\data\setupImg.jpg"): 
        os.remove("D:\Engage\streamlit\data\setupImg.jpg")
    else:
        print("The file does not exist")
    


placeholder = st.empty()
userImg = None
with placeholder.container():
    
    st.title("Introducing CAMFORT 1.0.0")
    col1, col2 = st.columns(2)
    with col1:
        st.text('\n')
        st.text('\n')
        page = st.radio("Start A Fresh Session",("Yep", "Nope"))
        st.text('\n')
        st.text('\n')
        st.text('\n')
        st.text('*The selected option will be chosen after \n 5 seconds')
    with col2:
        st.image("data/logo.jpg")
    
    time.sleep(5)
st.snow()
placeholder.empty()


if page == "Yep": 
    #cleanDatabase()
    #print('database cleaned')
    #cleanImgs()
    #print('Setup Image cleaned')
    #print('New session started')

    with placeholder.container():
                
        st.title("CamFort")
        run = st.checkbox('Click a picture in your ideal working state. Don\'t forget to Smile! ',value = True)
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

