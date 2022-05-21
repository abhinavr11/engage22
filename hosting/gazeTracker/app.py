from flask import Flask, jsonify, request, render_template
import pickle
import cv2
import joblib 
from helperGazeTrack import *
import json 
import numpy as np
from json import JSONEncoder
import warnings
warnings.filterwarnings('ignore')
#from Model import *

# load model
if __name__=='__main__':
    pass
    
# app
app = Flask(__name__)

# routes

@app.route('/')
def home():
    return render_template('index.html')
    
@app.route('/', methods=['POST'])

def predict():
    # get data
    data = request.get_json(force=True)
    
    # convert data into list
    #print(np.asarray(data['raw_img']).shape)

    # predictions
    eyePos = processEyePos(np.asarray(data['raw_img']).astype(np.uint8))
    print(eyePos)
    # send back to browser
    gazeTrackData = {"eyePos": [eyePos]} 
    # return data 
    return jsonify(results=gazeTrackData)


if __name__ == '__main__':
    app.run(port =5050, debug=True)