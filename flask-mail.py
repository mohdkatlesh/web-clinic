







@app.route('/')
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




if __name__ == '__main__':
	app.run(host="127.0.0.1", port=5050, debug=True)
