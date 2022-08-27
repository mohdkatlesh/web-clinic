
model = load_model("covid_model.h5", custom_objects={'tf': tf})
print('Model loaded. Check http://127.0.0.1:5001/')


def preprocess_image(image, target_size):
    if image.mode != "RGB":
        image = image.convert("RGB")
    image = image.resize(target_size)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    return image




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
