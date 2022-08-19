
from ctypes.wintypes import tagMSG
from tkinter import Y
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from tensorflow.keras.preprocessing.image import img_to_array


from tensorflow.keras.models import model_from_json
from tensorflow.python.framework import ops
ops.reset_default_graph()
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.models import load_model
import tensorflow as tf
import numpy as np
import h5py
from PIL import Image
import os


app = Flask(__name__)



model = load_model('kaggle', custom_objects={'tf': tf})
print('Model loaded. Check http://127.0.0.1:5000/')

def preprocess_image(image, target_size):
    if image.mode != "RGB":
        image = image.convert("RGB")
    image = image.resize(target_size)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = image/255.0
    return image

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


@app.route('/', methods=['GET'])
def index():
	return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def upload():

	classes = [
							'Pleural Effusion', 
							'Pneumonia', 
							'Infiltration', 
							'Nodule', 
							'Emphysema', 
							'Normal', 
							'Atelectasis', 
							'Pleural_Thickening', 
							'Pneumothorax', 
							'Atelectasis', 
							'Cystic Fibrosis', 
							'Emphysema', 
							'Pneumothorax', 
							'Pneumonia' 
	]



	if request.method == 'POST':

		# Get the file from post request
		f = request.files['file']

		# Save the file to ./uploads
		basepath = os.path.dirname(__file__)
		file_path = os.path.join(
			basepath, 'uploads', secure_filename(f.filename))
		f.save(file_path)

		# Make a prediction
		prediction = model_predict(file_path, model)

		print(np.argmax(prediction,axis=1))
		# response = np.array_str(np.argmax(prediction,axis=1))
		print(np.argmax(prediction))
		response = classes[np.argmax(prediction)]
		print(prediction)
		return response	




if __name__ == '__main__':
	app.run(debug = True)