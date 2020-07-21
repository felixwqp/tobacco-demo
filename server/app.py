from flask import Flask
import flask
from contour_detection import start
import cv2 as cv
app = Flask(__name__)


@app.route('/name/<filename>', methods=['GET'])
def hello(filename):
    image = cv.imread(filename)
    print(filename)
    print("!!!")
    res =start(image)
    print(res)
    # res = {"a":"b"}
    response = flask.jsonify(res)
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response
    # return "Hello World!"

if __name__ == '__main__':
    app.run()