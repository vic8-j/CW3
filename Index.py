from flask import Flask, request, jsonify
from flask import render_template
from keras.models import load_model
from operator import itemgetter
import cv2
import numpy as np
import os
from BreedInfo import *


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg'])
app.config['JSON_SORT_KEYS'] = False
model_file = 'model/catbreed_model.h5'
upload_dir = "upload"


def allowed_file(filename):
    '''
    Verify file format by file extension.
    :param filename:
    :return:
    '''

    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def index():
    '''
    Display the home page.
    :return:
    '''

    return render_template('index.html')


@app.route('/photoUpload', methods=['POST'])
def upload_file():
    '''
    Receive the photo and return the predicted result.
    :return:
    '''

    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = file.filename
            up_dir = os.path.join(basedir, 'upload')
            file.save(os.path.join(up_dir, filename))
            results = breed_predict(filename)
            return jsonify(results)


def breed_predict(image_name):
    '''
    Load the photo by name, and predict its breed, and return a dictionary of results.
    :param image_name:
    :return:
    '''

    model = load_model(model_file)
    image = cv2.resize(cv2.imread("upload/" + image_name), (224, 224))
    image = np.asarray(image.astype("float32"))
    image = image / 255.
    image = image.reshape((1, 224, 224, 3))
    breed_prob = model.predict(image)[0]

    i = 0
    breed_results = []
    for breed in breeds:
        breed_item = {}
        breed_item["name"] = breed[0]
        breed_item["prob"] = round(breed_prob[i] * 100, 2)
        breed_item["desc"] = breed[1]
        breed_results.append(breed_item)
        i += 1

    breed_results = sorted(breed_results, key=itemgetter('prob'), reverse=True)

    return breed_results[:5]


if __name__ == '__main__':
    app.debug = True
    app.run()
