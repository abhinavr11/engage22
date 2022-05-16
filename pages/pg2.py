import streamlit as st
import cv2

class continueSession:

    def __init__(self):
        self.st = st
        self.face_cascade = cv2.CascadeClassifier('requirements/haarcascade_frontalface_default.xml')
        self.startPg()



    def startPg(self):
        self.st.text("page 2 starting")

        self.st.title("Webcam Application")
        monitor = self.st.checkbox('Monitor',value = True)
        FRAME_WINDOW_TEMP = self.st.image([])
        cam = cv2.VideoCapture(0)
        
        self.st.image(cv2.imread('data/setupImg.jpg'),width = 200)
        
        while monitor:
            ret, frame = cam.read()
            
            try:
                # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                # # Detect the faces
                # faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
                # # Draw the rectangle around each face
                # for (x, y, w, h) in faces:
                #     cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
            except:
                continue
            
            FRAME_WINDOW_TEMP.image(frame)
            
               
        else:            
            self.st.write('Photo Taken')
          

        
        

