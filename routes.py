from app import app, model_predict, chest_model, covid_model, covid_model
from flask import render_template, redirect, url_for, request
from flask_mail import Mail,Message

from werkzeug.utils import secure_filename
import os
import numpy as np

from app import mail
#main-page
@app.route("/")
def services():
	return render_template("patient-services.html")

#contact-form
@app.route('/contact-form')
def contact():
    title = "Contact with our Doctor"
    return render_template('contactform.html', title = title)


@app.route('/form', methods=["GET ", "POST"])
def form():
    
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    
    if not name and not email and not phone:
        error_st = "All Form Fields Required..."
        return render_template("fail.html", error_st = error_st)

    message = request.form.get("message")
    img = request.files.get("img")
    title = "Thank you"
    sent_from = 'e.clinic.syria@gmail.com'
    sent_to = ['mhdkalesh@gmail.com' , "Kindaasaqer@gmail.com"]
    sent_subject = "E-Clinic New Case to Dignosis"
    
    sent_body = """\
        "Dear All,"
            I hope you are doing well.\n
            There is new case to study, and There is the information you need.\n
            Name:  %s \n
            Email: %s \n
            Phone Number: %s \n
            The Message: %s \n
            The X-Ray Image: %s  \n
            
            \n
            """ % (name, email, phone, message, img)

    email_text = """\
    From: %s
    To: %s
    Subject: %s
    %s
    """ % (sent_from, ", ".join(sent_to), sent_subject, sent_body)
    
    msg = Message( recipients =['mhdkatlesh@gmail.com']) 
    msg.body = email_text
    mail.send(msg)
    
    return render_template('form.html', 
                        title = title,
                        name = name,
                        email = email,
                        phone = phone,
                        message = message,
                        img = img)


#Chest-dignosis
@app.route('/chest-dignosis', methods=['GET'])
def chest_dignosis():
	return render_template('chest-dignosis.html')

@app.route('/chest', methods=['GET', 'POST'])
def upload_chest():

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

		f = request.files['file']

		basepath = os.path.dirname(__file__)
		file_path = os.path.join(
			basepath, 'uploads chest', secure_filename(f.filename))
		f.save(file_path)

		prediction = model_predict(file_path, chest_model)

		print(np.argmax(prediction,axis=1))
	
		print(np.argmax(prediction))
		response = classes[np.argmax(prediction)]
		print(prediction)
		return response	


#covid_model
@app.route('/covid-dignosis', methods=['GET'])
def covid_dignosis():

    return render_template('covid-dignosis.html')


@app.route('/covid', methods=['GET', 'POST'])
def upload_covid():

    classes = ['conid-19', 'Normal', 'Pneumonia']

    if request.method == 'POST':

        f = request.files['file']

        basepath = os.path.dirname(__file__)
        file_path = os.path.join(basepath, 'uploads covid',
                                 secure_filename(f.filename))
        f.save(file_path)

        prediction = model_predict(file_path, covid_model)

        print(np.argmax(prediction, axis=1))
        # response = np.array_str(np.argmax(prediction,axis=1))
        print(np.argmax(prediction))
        response = classes[np.argmax(prediction)]
        print(prediction)
        return response
