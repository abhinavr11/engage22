from flask import Flask, jsonify, request, render_template
import pickle
import cv2
import joblib 
from helper import *
import json 
import numpy as np
from json import JSONEncoder
import warnings
warnings.filterwarnings('ignore')

class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)
#from Model import *

# load model
if __name__=='__main__':
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    
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
    print(np.asarray(data['raw_img']).shape)

    # predictions
    output,area = detectFace(np.asarray(data['raw_img']).astype(np.uint8))
    
    # send back to browser
    numpyData = {"processed_img": output,
                 "area":np.asarray(area)}
    encodedNumpyData = json.dumps(numpyData, cls=NumpyArrayEncoder)
    
    # return data 
    return jsonify(results=encodedNumpyData)


if __name__ == '__main__':
    app.run(port =5000, debug=True)