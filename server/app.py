from flask import Flask
import flask
from contour_detection import start
import cv2 as cv
from os import getcwd
import os
from dense import start_dense

app = Flask(__name__, static_url_path='/static')

def save_images(images_info, filename):
    new_infos = []
    for info in images_info:
        new_infos.append({'name': os.path.basename(info), 'filename':os.path.basename(info)})
    
    return new_infos



@app.route('/name/<filename>', methods=['GET'])
def hello(filename):
    image = cv.imread(filename)
    print(filename)
    print("!!!")
    res = start_dense()
    new_info = save_images(res['files_info'], filename)
    res['files_info'] = new_info
    print(res)
    # res = {"a":"b"}
    response = flask.jsonify(res)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    # return "Hello World!"

if __name__ == '__main__':
    app.run()