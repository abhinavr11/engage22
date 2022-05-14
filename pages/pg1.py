import streamlit as st

class newSession:

    def __init__(self):
        self.st = st

        self.startPg()

    def startPg(self):
        self.st.text("Page 1 starting")


