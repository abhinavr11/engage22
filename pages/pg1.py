import streamlit as st
import cv2

class newSession:

    def __init__(self):
        self.st = st
        self.run = True
        self.btn = None
        self.startPg()
        

    def startPg(self):
        self.st.text("Page 1 starting")
        

        

    def stopPg(self):
        self.run = False
        #self.FRAME_WINDOW = None


