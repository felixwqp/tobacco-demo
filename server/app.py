from flask import Flask, send_file
import flask
from contour_detection import start
import cv2 as cv
from os import getcwd

app = Flask(__name__, static_url_path='/static')

def save_images(images_info, filename):
    new_infos = []
    for info in images_info:
        cv.imwrite(getcwd() + "/static/" + filename + "_" + info['filename'], info['file'])
        new_infos.append({'name': info['name'], 'filename':filename+"_"+info['filename']})
    
    return new_infos



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
    res =start(image)
    new_info = save_images(res['files_info'], filename)
    res['files_info'] = new_info
    print(res)
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