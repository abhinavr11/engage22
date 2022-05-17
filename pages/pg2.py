import streamlit as st
import cv2
import json
from json import JSONEncoder
import requests
import numpy as np

class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


class continueSession:

    def __init__(self):
        self.st = st
        self.url = 'http://127.0.0.1:5000/'
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

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                numpyData = {"raw_img": frame}
                encodedNumpyData = json.dumps(numpyData, cls=NumpyArrayEncoder)
                res = requests.post(self.url, data = encodedNumpyData)

                frame = np.asarray(json.loads(res.json()['results'])['processed_img']) 
            except:
                continue
            
            FRAME_WINDOW_TEMP.image(frame)
            
               
        else:            
            self.st.write('Photo Taken')
          

        
        

