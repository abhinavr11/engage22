import streamlit as st


class newSession:

    def __init__(self):
        self.st = st
        self.startPg()
        

    def startPg(self):
        self.st.text("Sit Tight Loading ...")
        

    def stopPg(self):
        self.run = False
        


