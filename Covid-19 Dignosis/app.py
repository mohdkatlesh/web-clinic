from ctypes.wintypes import tagMSG
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from tensorflow.keras.preprocessing.image import img_to_array

from tensorflow.keras.models import model_from_json
from tensorflow.python.framework import ops

ops.reset_default_graph()
from keras.preprocessing import image
from keras.preprocessing.image import load_img
from tensorflow.keras.models import load_model
import tensorflow as tf
# Import other dependecies
import numpy as np
import h5py
from PIL import Image
import PIL
import os

app = Flask(__name__)

model = load_model("covid_model.h5", custom_objects={'tf': tf})
print('Model loaded. Check http://127.0.0.1:5001/')


def preprocess_image(image, target_size):
    if image.mode != "RGB":
        image = image.convert("RGB")
    image = image.resize(target_size)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    return image


def model_predict(img_path, model):

    IMG = load_img(img_path).convert('L')
    print(type(IMG))

    # Pre-processing the image
    # IMG_ = IMG.resize((600, 600))
    # print(type(IMG_))
    # IMG_ = np.asarray(IMG_)
    # print(IMG_.shape)
    # IMG_ = np.true_divide(IMG_, 255)
    # IMG_ = IMG_.reshape(1, 600, 600, 1)
    # print(type(IMG_), IMG_.shape)
    IMG_ = preprocess_image(IMG, target_size=(224, 224))

    print(model)

    model.compile(loss='categorical_crossentropy',
                  metrics=['accuracy'],
                  optimizer='rmsprop')
    prediction = model.predict(IMG_)

    return prediction


@app.route('/', methods=['GET'])
def index():

    return render_template('index.html')


@app.route('/covid', methods=['GET', 'POST'])
def upload():

    classes = ['conid-19', 'Normal', 'Pneumonia']

    if request.method == 'POST':

        f = request.files['file']

        basepath = os.path.dirname(__file__)
        file_path = os.path.join(basepath, 'uploads',
                                 secure_filename(f.filename))
        f.save(file_path)

        prediction = model_predict(file_path, model)

        print(np.argmax(prediction, axis=1))
        # response = np.array_str(np.argmax(prediction,axis=1))
        print(np.argmax(prediction))
        response = classes[np.argmax(prediction)]
        print(prediction)
        return response


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5001, debug=True)
