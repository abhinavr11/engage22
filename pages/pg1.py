import streamlit as st
import cv2

class newSession:

    def __init__(self):
        self.st = st
        self.startPg()
        

    def startPg(self):
        self.st.text("Sit Tight Loading ...")
        

        

    def stopPg(self):
        self.run = False
        #self.FRAME_WINDOW = None


