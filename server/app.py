from flask import Flask, send_file
import flask
from contour_detection import start
import cv2 as cv
from PIL import Image
from dense import start_dense
import numpy as np
import io
import os
import glob

import flickrapi
import csv
import requests

# api_key = '68d7cbd37b544fb8cb4c5049c87064f3'
# api_secret = '9322150cc690156f'
# flickr = flickrapi.FlickrAPI(api_key, api_secret)
# flickr.authenticate_via_browser(perms='delete')

# def uploadPhoto(path_photo, title, description, tags):
#     result=False
#     with open(path_photo, 'rb') as f:
#         photo = {'file': f}
#         try:    
#             result = requests.post('https://up.flickr.com/services/upload/', data = {'photo':'photo', 'title':'title', 'description':'description', 'tags':'tags'})
#             print(result.text)
#         except Exception as error:
#             print('Upload photo', error, '--- o --- titulo malo -> ', title)        
#     return result


app = Flask(__name__)


# @app.route('/name/<filename>', methods=['GET'])
# def hello(filename):
#     image = cv.imread(filename)
#     print(filename)
#     print("!!!")
#     res =start(image)
#     print(res)
#     # res = {"a":"b"}
#     response = flask.jsonify(res)
#     response.headers.add('Access-Control-Allow-Origin', '*')

#     return response
#     # return "Hello World!"

@app.route('/name/<filename>', methods=['GET'])
def hello(filename):
    image = cv.imread(filename)
    print(filename)
    print("!!!")
    # start_dense()
    # res = {"a":"b"}
    imgs = glob.glob(os.path.join("Width", "*.jpg"))
    results = list()
    for idx, img in enumerate(imgs):
        results.append({"path": os.path.abspath(img), "id": idx})
    response = flask.jsonify(results)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


if __name__ == '__main__':
    app.run()