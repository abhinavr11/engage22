from time import sleep
import streamlit as st
import cv2
import json
from json import JSONEncoder
import requests
import numpy as np
import collections
import threading

class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


class continueSession:

    def __init__(self):
        self.st = st
        self.url = 'http://127.0.0.1:5000/'
        self.cpos = cv2.imread('data/rpos.jpg')
        self.wpos = cv2.imread('data/wpos.jpg')
        self.pos = cv2.imread('data/rpos.jpg')
        self.setupImg = cv2.imread('data/setupImg.jpg')
        self.poseBuffer = collections.deque(maxlen=1)
        temp = self.getSetupArea(self.setupImg)
        print(temp)
        self.setupArea = temp
        

        self.startPg()

    def startPg(self):
        self.st.text("page 2 starting")
        self.st.title("Webcam Application")
        monitor = self.st.checkbox('Monitor',value = True)
        
        FRAME_WINDOW_TEMP = self.st.image([])
        self.st.image(self.setupImg,width = 200)
        cam = cv2.VideoCapture(0)
        
        
        t1 = threading.Thread(target=self.poseThread)
        t1.start()
        #i = 0
        while monitor:
            ret, frame = cam.read()
            
            try:

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.poseBuffer.append(frame)
                
                # if i == 10:
                    
                #     numpyData = {"raw_img": frame}
                #     encodedNumpyData = json.dumps(numpyData, cls=NumpyArrayEncoder)
                #     res = requests.post(self.url, data = encodedNumpyData)
                #     resp = json.loads(res.json()['results'])
                #     frame = np.asarray(resp['processed_img']) 
                    
                #     if resp['area'] > self.setupArea:
                #         self.pos = self.wpos
                #     else:
                #         self.pos = self.cpos
                #     i=0
            
            except:
                continue
            
            #i += 1
            FRAME_WINDOW_TEMP.image([frame,self.pos])
            
            
               
        else:            
            self.st.write('Photo Taken')
          
        t1.join()
        
    def getSetupArea(self,img):
        numpyData = {"raw_img": img}
        encodedNumpyData = json.dumps(numpyData, cls=NumpyArrayEncoder)
        res = requests.post(self.url, data = encodedNumpyData)
        resp = json.loads(res.json()['results'])
        return resp['area']

    def poseThread(self):
        while(True):
            if self.poseBuffer:
               
                numpyData = {"raw_img": self.poseBuffer[0]}
                encodedNumpyData = json.dumps(numpyData, cls=NumpyArrayEncoder)
                res = requests.post(self.url, data = encodedNumpyData)
                if res.status_code == 200:
                    resp = json.loads(res.json()['results'])
                else:
                    continue
                #frame = np.asarray(resp['processed_img']) 
                
                if resp['area'] > self.setupArea:
                    self.pos = self.wpos
                else:
                    self.pos = self.cpos
                
                #self.poseBuffer.popleft()

            else:
                continue

