from time import sleep
import streamlit as st
import cv2
import json
from json import JSONEncoder
import requests
import numpy as np
import collections
import threading
from PIL import Image , ImageStat

class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


class continueSession:

    def __init__(self):
        self.st = st
        self.urlFace = 'http://127.0.0.1:5000/'
        self.urlEye = 'http://127.0.0.1:5050/'
        self.cpos = cv2.imread('data/rpos.jpg')
        self.wpos = cv2.imread('data/wpos.jpg')
        self.pos = cv2.imread('data/rpos.jpg')
        self.eyePosW = cv2.imread('data/working.jpg')
        self.eyePosD = cv2.imread('data/dreaming.jpg')
        self.setupImg = cv2.imread('data/setupImg.jpg')
        self.eyePos = cv2.imread('data/working.jpg')
        self.brightness = 0
        self.frameBuffer = collections.deque(maxlen=1)
        temp = self.getSetupArea(self.setupImg)
        self.setupArea = temp
        

        self.startPg()

    def startPg(self):
        self.st.text("page 2 starting")
        self.st.title("Webcam Application")
        monitor = self.st.checkbox('Monitor',value = True)
        
        FRAME_WINDOW_TEMP = self.st.image([])
        self.bar = self.st.progress(0)
        self.st.image(self.setupImg,width = 100)
        cam = cv2.VideoCapture(0)
        
        
        t1 = threading.Thread(target=self.poseThread)
        t2 = threading.Thread(target=self.brightnessThread)
        t3 = threading.Thread(target=self.gazeTrackerThread)
        t1.start()
        t2.start()
        t3.start()
        
        while monitor:
            ret, frame = cam.read()    
            try:

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.frameBuffer.append(frame)
                
            
            except:
                continue
            self.bar.progress(self.brightness)
            FRAME_WINDOW_TEMP.image([frame,self.pos,self.eyePos],width= 300)
            
    
               
        else:            
            self.st.write('We can show the statistics here')
          
        t1.join()
        t2.join()
        t3.join()




        
    def getSetupArea(self,img):
        numpyData = {"raw_img": img}
        encodedNumpyData = json.dumps(numpyData, cls=NumpyArrayEncoder)
        res = requests.post(self.urlFace, data = encodedNumpyData)
        resp = json.loads(res.json()['results'])
        return resp['area']

    def poseThread(self):
        while(True):
            if self.frameBuffer:
               
                numpyData = {"raw_img": self.frameBuffer[0]}
                encodedNumpyData = json.dumps(numpyData, cls=NumpyArrayEncoder)
                res = requests.post(self.urlFace, data = encodedNumpyData)
                if res.status_code == 200:
                    resp = json.loads(res.json()['results'])
                else:
                    continue
                #frame = np.asarray(resp['processed_img']) 
                
                if resp['area'] > self.setupArea:
                    self.pos = self.wpos
                else:
                    self.pos = self.cpos
                
                

            else:
                continue

    def brightnessThread(self):

        while True:
            if self.frameBuffer:
            
                self.brightness = ImageStat.Stat(Image.fromarray(np.asarray(self.frameBuffer[0]))).mean[0]/255
            else:
                continue
                
    def gazeTrackerThread(self):
        while(True):
            if self.frameBuffer:
               
                numpyData = {"raw_img": self.frameBuffer[0]}
                encodedNumpyData = json.dumps(numpyData, cls=NumpyArrayEncoder)
                res = requests.post(self.urlEye, data = encodedNumpyData)
                if res.status_code == 200:
                    resp = res.json()['results']
                else:
                    continue
                #frame = np.asarray(resp['processed_img']) 
                
                #print(resp['eyePos'][0])

                if resp['eyePos'][0][0] != 'CENTRE' and  resp['eyePos'][0][1] != 'CENTRE':
                    self.eyePos = self.eyePosD
                else:
                    self.eyePos = self.eyePosW
                
                

            else:
                continue




