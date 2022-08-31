from flask import Flask, render_template
from flask_mail import Mail,Message
from tensorflow.keras.models import model_from_json
from tensorflow.python.framework import ops
ops.reset_default_graph()
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.models import load_model
import tensorflow as tf
import numpy as np
import h5py
from PIL import Image
import os

app = Flask(__name__)


app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'e.clinic.syria@gmail.com'
app.config['MAIL_PASSWORD'] = 'sbsfytnxgmvrcijh'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER'] = 'e.clinic.syria@gmail.com'
mail = Mail(app)

#covid-dignosis
covid_model = load_model("Covid-19 Dignosis/covid_model.h5", custom_objects={'tf': tf})


#chest-dignosis
chest_model = load_model('Chest Dignosis/kaggle_seresnet.h5', custom_objects={'tf': tf})

#proccessing_the_image
def preprocess_image(image, target_size):
    if image.mode != "RGB":
        image = image.convert("RGB")
    image = image.resize(target_size)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = image/255.0
    return image

#chest_prediction
def model_predict(img_path, model):

	IMG = load_img(img_path).convert('L')
	print(type(IMG))

	IMG_ = IMG.resize((600, 600))
	print(type(IMG_))
	IMG_ = np.asarray(IMG_)
	print(IMG_.shape)
	IMG_ = np.true_divide(IMG_, 255)
	print(type(IMG_), IMG_.shape)
	IMG_ = preprocess_image(IMG, target_size=(600,600))

	print(model)

	model.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer='rmsprop')
	prediction = model.predict(IMG_)
	return prediction

#covid_prediction
def model_predict(img_path, covid_model):

    IMG = load_img(img_path).convert('L')
    IMG_ = IMG.resize((600,
     600))
    IMG_ = np.asarray(IMG_)
    IMG_ = np.true_divide(IMG_, 255)
    IMG_ = IMG_.reshape(1, 600, 600, 1)
    IMG_ = preprocess_image(IMG, target_size=(224, 224))

    
    covid_model.compile(loss='categorical_crossentropy',
                  metrics=['accuracy'],
                  optimizer='rmsprop')
    prediction = covid_model.predict(IMG_)

    return prediction



from routes import *


if __name__ == '__main__':
	app.run(debug = True)