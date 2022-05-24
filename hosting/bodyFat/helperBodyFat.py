import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
from tensorflow.keras.models import Sequential
from keras.layers import Input, Dense, Dropout, Flatten, Conv2D, MaxPooling2D, BatchNormalization, LeakyReLU
import pandas as pd
import cv2
import os


model = tf.keras.models.load_model("model.h5")                     #For BMI prediction
model2 = tf.keras.models.load_model("model2.h5")                   #For Age prediction
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
   
def predictBodyFat(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Detect the faces
    faces = face_cascade.detectMultiScale(gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE)
    # Draw the rectangle around each face
    for (x, y, w, h) in faces:
        face_frame = cv2.resize(image[x:x+h,y:y+h,:], (224, 224))
    
    
    face_frame = face_frame.reshape(1,224,224,3)
    bmi = model.predict(face_frame)[0][0]
    age = model2.predict(face_frame)[0][0]
    body_fat = 1.2*bmi + 0.23*age - 5.4

    return body_fat

