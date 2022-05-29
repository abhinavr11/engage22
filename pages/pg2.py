from time import sleep
from turtle import width
import streamlit as st
import cv2
import json
from json import JSONEncoder
import requests
import numpy as np
import collections
import threading
import time
import pymongo
import pandas as pd
from PIL import Image , ImageStat
from datetime import datetime, timedelta

FRAMES_PROCESSED = 20    #Kept as constant the number of frames that need to be processed before data is pushed to the database

#Class to help encode images before they are sent to the hosted models
class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

#Main class of the session that is being continued
class continueSession:

    def __init__(self):
        self.st = st
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mydb = self.myclient['masterdatabase']
        self.urlFace = 'http://127.0.0.1:5000/'
        self.urlEye = 'http://127.0.0.1:5050/'
        self.urlFat = 'http://127.0.0.1:5100/'
        self.cpos = cv2.imread('data/rpos.png')
        self.wpos = cv2.imread('data/wpos.png')
        self.pos = cv2.imread('data/rpos.png')
        self.eyePosW = cv2.imread('data/working.png')
        self.eyePosD = cv2.imread('data/dreaming.png')
        self.setupImg = cv2.imread('data/setupImg.jpg')
        self.eyePos = cv2.imread('data/working.png')
        self.pose_text = 'Maintain this posture'
        self.eye_text = 'Your eyes are on the goal'
        self.brightness = 0
        self.frameBuffer = collections.deque(maxlen=1)
        temp = self.getSetupArea(self.setupImg)
        self.setupArea = temp
        self.sessionTime = datetime.now()
        self.poseVar = np.zeros(3)
        self.fatVar = np.zeros(2)
        self.lightVar = np.zeros(2)
        self.focusVar = np.zeros(3)
        

        self.startPg()

    def startPg(self):
        col1, col2 = self.st.columns(2)
        with col1:
            self.st.title("CamFort")
            FRAME_TEXT_TEMP = self.st.text('')
       
        with col2:
            self.st.header("👩‍💻WORK RIGHT🧑‍💻")
            
        monitor = self.st.checkbox('Monitor',value = True)
        FRAME_WINDOW_TEMP_CAM = self.st.image([])
        col1, col2 = self.st.columns(2)
        with col1:
            self.st.header('Current Posture')
            FRAME_WINDOW_TEMP_POSE = self.st.image([])
            FRAME_TEXT_TEMP_POSE = self.st.text('')
        with col2:
            self.st.header('Eye Tracker')
            FRAME_WINDOW_TEMP_EPOS = self.st.image([])
            FRAME_TEXT_TEMP_EPOS = self.st.text('')
        self.st.header('Lighting')
        self.bar = self.st.progress(0)
        self.st.text('-----------(Low Lighting)-------------Optimum-------------(Bright Lighting)--------')
        #self.st.image(self.setupImg,width = 100)
        cam = cv2.VideoCapture(0)
        
        
        t1 = threading.Thread(target=self.poseThread)
        t2 = threading.Thread(target=self.brightnessThread)
        t3 = threading.Thread(target=self.gazeTrackerThread)
        t4 = threading.Thread(target=self.bodyFatThread)
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        
        while monitor:
            ret, frame = cam.read()    
            try:

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.frameBuffer.append(frame)
                
            
            except:
                continue
            self.bar.progress(self.brightness)
            FRAME_WINDOW_TEMP_CAM.image([frame],width= 400)
            FRAME_WINDOW_TEMP_POSE.image([self.pos],width= 300)
            FRAME_WINDOW_TEMP_EPOS.image([self.eyePos],width= 300)
            FRAME_TEXT_TEMP.text('Session Runtime ⏲️ '+str(datetime.now()-self.sessionTime)) 
            FRAME_TEXT_TEMP_EPOS.text(self.eye_text)
            FRAME_TEXT_TEMP_POSE.text(self.pose_text)
            
            
    
               
        else:            
            self.st.title('The Boring statistics')
            myclient = pymongo.MongoClient("mongodb://localhost:27017/")
            mydb = myclient['masterdatabase']

            with st.spinner('Evaluating Statistics'):
    

                showFat = self.__getBodyFatDF(pd.DataFrame(list(mydb['BodyFat'].find())))
                showFocus = self.__getAttentionDF(pd.DataFrame(list(mydb['Attention'].find())))
                showBright = self.__getLuminosityDF(pd.DataFrame(list(mydb['Luminosity'].find())))
                showPose = self.__getPostureDF(pd.DataFrame(list(mydb['Posture'].find())))

                self.st.area_chart(showFat)
                self.st.bar_chart(showFocus)
                self.st.line_chart(showBright)
                self.st.bar_chart(showPose)
            st.success('Done!')
        
        t1.join()
        t2.join()
        t3.join()
        t4.join()



    #Functions of the class , names are explanatory of the work they do
        
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
                    self.pose_text = 'Straighten your back please!'
                    self.poseVar[0] += 1
                    self.poseVar[2] += 1
                else:
                    self.pos = self.cpos
                    self.pose_text = 'Maintain this posture'
                    self.poseVar[0] += 1
                    self.poseVar[1] += 1
                
                if self.poseVar[0] >= FRAMES_PROCESSED:
                    col = self.mydb['Posture']
                    dat ={'time':datetime.now(),
                    'right_pose':self.poseVar[1],
                    'wrong_pose':self.poseVar[2],
                    'total_reading':self.poseVar[0]
                    }
                    _ = col.insert_one(dat)
                    self.poseVar = np.zeros(3)

            else:
                continue

    def brightnessThread(self):

        while True:
            if self.frameBuffer:
            
                self.brightness = ImageStat.Stat(Image.fromarray(np.asarray(self.frameBuffer[0]))).mean[0]/255

                self.lightVar[0] += 1
                self.lightVar[1] += self.brightness

                if self.lightVar[0] >= FRAMES_PROCESSED**2:
                    col = self.mydb['Luminosity']
                    dat ={'time':datetime.now(),
                    'brightness':self.lightVar[1],
                    'total_reading':self.lightVar[0]
                    }
                    _ = col.insert_one(dat)
                    self.lightVar = np.zeros(2)

            
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
                    self.eye_text = 'Don\'t get distracted'
                    self.focusVar[0] += 1
                    self.focusVar[2] += 1

                else:
                    self.eyePos = self.eyePosW
                    self.eye_text = 'Your eyes are on the goal'
                    self.focusVar[0] += 1
                    self.focusVar[1] += 1

                if self.focusVar[0] >= FRAMES_PROCESSED:
                    col = self.mydb['Attention']
                    dat ={'time':datetime.now(),
                    'focused':self.focusVar[1],
                    'not_focused':self.focusVar[2],
                    'total_reading':self.focusVar[0]
                    }
                    _ = col.insert_one(dat)
                    self.focusVar = np.zeros(3)


            else:
                continue


    def bodyFatThread(self):
        while(True):
            time.sleep(3600)                #Body fat prections are measured and stored after an hour
            if self.frameBuffer:
               
                numpyData = {"raw_img": self.frameBuffer[0]}
                encodedNumpyData = json.dumps(numpyData, cls=NumpyArrayEncoder)
                res = requests.post(self.urlFat, data = encodedNumpyData)
                if res.status_code == 200:
                    resp = res.json()['results']
                else:
                    continue
                
                self.fatVar[0] += 1
                self.fatVar[1] += resp['bodyFat'][0]

                if self.fatVar[0] >= FRAMES_PROCESSED:
                    col = self.mydb['BodyFat']
                    dat ={'time':datetime.now(),
                    'fat':self.fatVar[1],
                    'total_reading':self.fatVar[0]
                    }
                    _ = col.insert_one(dat)
                    self.fatVar = np.zeros(2)
                    

            else:
                continue


    def __getBodyFatDF(self,data):
        showFat = {
            'Time':[dt[1]['time'] for dt in data.iterrows()],
            'Average Fat':[dt[1]['fat']/dt[1]['total_reading'] for dt in data.iterrows()]
        }

        return pd.DataFrame(showFat).set_index('Time')

    def __getAttentionDF(self,data):
        timeDelta = []
        focused = []
        nfocused = []
        for idx,dt in data.iterrows():
            if idx == 0:
                continue
            timeDelta.append((dt['time']-data.loc[idx-1]['time']).seconds)
            focused.append(100*dt['focused']/dt['total_reading'])
            nfocused.append(100*dt['not_focused']/dt['total_reading'])
            
        showFocus = {
            'Time':timeDelta,
            'Focused %':focused,
            'Not Focused %':nfocused
        } 
        return pd.DataFrame(showFocus).set_index('Time')

    def __getLuminosityDF(self,data):
        showBright = {
            'Time':[dt[1]['time'] for dt in data.iterrows()],
            'Average Brightness':[dt[1]['brightness']/dt[1]['total_reading'] for dt in data.iterrows()]
        }

        return pd.DataFrame(showBright).set_index('Time')

    def __getPostureDF(self,data):
        timeDelta = []
        rposePer = []
        wposePer = []
        for idx,dt in data.iterrows():
            if idx == 0:
                continue
            timeDelta.append((dt['time']-data.loc[idx-1]['time']).seconds)
            rposePer.append(100*dt['right_pose']/dt['total_reading'])
            wposePer.append(100*dt['wrong_pose']/dt['total_reading'])
            
        showPose = {
            'Time':timeDelta,
            'Correct Pose %':rposePer,
            'Wrong Pose %':wposePer
        } 
        return pd.DataFrame(showPose).set_index('Time')