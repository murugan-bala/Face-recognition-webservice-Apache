import cv2
import flask
import face_recognition
import glob
import os
import logging
import time
import re
import json
import sys
import flask
import datetime
import requests
import base64
import numpy as np
import face_recognition
from flask import Flask, send_file
from flask import request
from flask import jsonify
from waitress import serve
from flask_cors import CORS
from PIL import Image, ImageDraw
#from ocrr import tesseract
#from text_tesseract import tess
app = Flask(__name__)
CORS(app)
CAMERA_DEVICE_ID = 0
MAX_DISTANCE = 0.6  # increase to make recognition less strict, decrease to make more strict

def face_distance_to_conf(face_distance, face_match_threshold=0.60):
    if face_distance > face_match_threshold:
        range = (1.0 - face_match_threshold)
        linear_val = (1.0 - face_distance) / (range * 2.0)
        return linear_val
    else:
        range = face_match_threshold
        linear_val = 1.0 - (face_distance / (range * 2.0))
        return linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))





def get_face_embeddings_from_image(image, convert_to_rgb=False):
    """
    Take a raw image and run both the face detection and face embedding model on it
    """
    # Convert from BGR to RGB if needed
    if convert_to_rgb:
        image = image[:, :, ::-1]

    # run the face detection model to find face locations
    face_locations = face_recognition.face_locations(image)

    # run the embedding model to get face embeddings for the supplied locations
    face_encodings = face_recognition.face_encodings(image, face_locations)

    return face_locations, face_encodings

#Note: OpenCV reads images in BGR format, face_recognition in RGB format, so sometimes you need to convert them, sometimes no



def paint_detected_face_on_image(frame, location, name=None):
    """
    Paint a rectangle around the face and write the name
    """
    # unpack the coordinates from the location tuple
    top, right, bottom, left = location
    if name is None:
        #count_starts = time.time()
        #name = 'Unknown'
        name = 'Face'
        color = (0, 0, 255)  # red for unrecognized face
    else:
        #count_end = time.time()
        color = (0, 128, 0)  # dark green for recognized face
    #timee=count_starts-count_end
    #print(timee)
    # Draw a box around the face
    cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

    # Draw a label with a name below the face
    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
    cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)

global i
i=0
error_status=""
@app.route('/',methods = ['POST','GET'])
def homepage():
    #return "Welcome to AIML service..."
    return jsonify({'welcome' :"Hi Welcomeee....!!!!"})

error_status="Sucess"
@app.route('/face_validation',methods = ['POST','GET'])
def face_validation():
    #print("verifyPhoto.face_detection: {}".format("Entered service method"),flush=True)
    print("Hello")
    result="No faces detected"
    ocr="None"
    words="None"
    output=""
    error_code=0
    error_status="Sucess"
    if request.method == 'POST':
        try:
         #result="No faces detected"
             #output="invalid"
             error_status="Sucess"
             print("Hellooooo face_validation")
             result="No faces detected"
             #file = request.files['file']
             req_json=request.json
             #print("face_detection.req_json: {}".format(req_json),flush=True)
             #print(type(req_json))
             if 'img1' in request.json:   #{"compare":"sucess"}
                req_json=request.json
                #print("inside validate..")
                #print("face_detection.req_json: {}".format(req_json),flush=True)
                #print(type(req_json))
                #print(req_json['img1'])
                img_name=req_json['filename']
		print(img_name)
                s=req_json['img1']
                x = s.split(",")
                #print(len(x))
                #print(x[1])
                encod_img1=x[1].encode()
                #encod_img1=req_json['img1'][18:].encode()
                #print(req_json['img1'][18:])  #iV
                image1_decode = base64.decodestring(encod_img1)
                with open('/var/www/html/FlaskApp/'+img_name, 'wb') as image1_result:
                    image1_result.write(image1_decode)
                unknown_image = face_recognition.load_image_file('/var/www/html/FlaskApp/'+img_name)
                face_locations = face_recognition.face_locations(unknown_image) #face_locations = face_recognition.face_locations(image, model="cnn")
                print("There are ",len(face_locations),"people in this image")
                #result="single faces detected"
                img = cv2.imread('/var/www/html/FlaskApp/'+img_name, cv2.IMREAD_GRAYSCALE)   # my_photo, incorrect_3
                n_white_pix = np.sum(img == 255)
                print("Gray image shape is :",img.shape)
                print("Total pixels is (gray image ) :",img.size)
                print('Number of white pixels:', n_white_pix)

                if n_white_pix >50000:
                    print("Photo is not valid..")
                    result="Scaned faces detected"
                    output="invalid"
                    error_code=0
                else:
                    print("Valid photo..")
                    if len(face_locations)==0:
                        print("No Faces Detected..")
                        result="No faces detected"
                        output="invalid"
                        error_code=0
                    elif len(face_locations)>1:
                        print("More than One Face detected....")
                        result="More faces detected"
                        output="invalid"
                        error_code=2
                    elif len(face_locations)==1:
                        print("Single Face detected....")
                        result="single faces detected"
                        output="valid"
                        error_code=1
        except Exception as e:
            print(e)
            error_status=e
            result="Error Occured..."
            output="invalid"
            print("Error occured ....")
            error_code=0
    try:
	os.remove('/var/www/html/FlaskApp/'+img_name)
    except:
	print("Can not delete the image file as it doesn't exists")
    return jsonify({'output' : output,'result':result,'error_code':error_code,'error_status':error_status})

@app.route('/sign_validation',methods = ['POST','GET'])
def sign_validation():
    #print("verifyPhoto.face_detection: {}".format("Entered service method"),flush=True)
    print("Hello")
    result="In-Valid Signature"
    ocr="None"
    words="None"
    output=""
    error_code=0
    error_status="Sucess"
    if request.method == 'POST':
        try:
         #result="No faces detected"
             #output="invalid"
             error_status="Sucess"
             print("Hellooooo sign_validation")
             result="No faces detected"
             #file = request.files['file']
             req_json=request.json
             #print("face_detection.req_json: {}".format(req_json),flush=True)
             #print(type(req_json))
             if 'img1' in request.json:   #{"compare":"sucess"}
                req_json=request.json
                #print("inside validate..")
                #print("face_detection.req_json: {}".format(req_json),flush=True)
                #print(type(req_json))
                #print(req_json['img1'])
                img_name=req_json['filename']
                s=req_json['img1']
                x = s.split(",")
                #print(len(x))
                #print(x[1])
                encod_img1=x[1].encode()
                #encod_img1=req_json['img1'][18:].encode()
                #print(req_json['img1'][18:])  #iV
                image1_decode = base64.decodestring(encod_img1)
                with open('/var/www/html/FlaskApp/'+img_name, 'wb') as image1_result:
                    image1_result.write(image1_decode)
                unknown_image = face_recognition.load_image_file('/var/www/html/FlaskApp/'+img_name)
                face_locations = face_recognition.face_locations(unknown_image) #face_locations = face_recognition.face_locations(image, model="cnn")
                img = cv2.imread('/var/www/html/FlaskApp/'+img_name, cv2.IMREAD_GRAYSCALE)   # my_photo, incorrect_3
                n_white_pix = np.sum(img == 255)
                #print("Gray image shape is :",img.shape)
                #print("Total pixels is (gray image ) :",img.size)
                print('Number of white pixels:', n_white_pix)
                print("There are ",len(face_locations),"people in this image")
                result="single faces detected"
                error_code=1
                if n_white_pix >50000:
                    #now = time.strftime('%d-%m-%Y %H:%M:%S')
                    print("signature is not valid..")
                    error_code=0
                    result="Invalid"
                    #printt('In_Valid signature detected : {}'.format(file))
                    #printt('{}  : signature not detected : {}'.format(now,file))
                    #in_valid=in_valid+1
                    #csvwriter.writerows([[now, file_name[-1]]])
                else:
                    #print("Valid photo..")
                    if len(face_locations)==0:
                        print("Valid Signature..")
                        result="Valid"
                        error_code=1
                    elif len(face_locations)>0:
                        print("Invalid signature........")
                        result="Invalid"
                        error_code=0
                '''img = cv2.imread('validation.jpg', cv2.IMREAD_GRAYSCALE)   # my_photo, incorrect_3
                n_white_pix = np.sum(img == 255)
                print("Gray image shape is :",img.shape)
                print("Total pixels is (gray image ) :",img.size)
                print('Number of white pixels:', n_white_pix)

                if n_white_pix >50000:
                    print("Photo is not valid..")
                    output="invalid"
                else:
                    print("Valid photo..")
                    output="valid"'''
        except Exception as e:
            output="invalid"
            error_status=e
            result="error occured.."
            print("Error occured ....")
            error_code=0
    try:
	os.remove('/var/www/html/FlaskApp/'+img_name)
    except:
	print("Can not delete the image file as it doesn't exists")
    return jsonify({'result':result,'error_code':error_code,'error_status':error_status})
#if __name__ == '__main__':
    #context = ('/etc/ssl/certs/my.crt', '/etc/ssl/private/my.key')#certificate and key files
    #app.run(host='0.0.0.0',port=5022 ,debug=True,ssl_context=context,threaded=True)
    #app.run(host='0.0.0.0',port=5023,debug=True)


