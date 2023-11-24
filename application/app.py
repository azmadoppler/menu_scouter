from flask import Flask, request, render_template, redirect, url_for
import os

app = Flask(__name__)

# Ensure there is a folder named 'uploads' in the same directory as this script
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return 'No selected file'

        if file:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)

            # Here you would typically pass the filename to your
            # image classification model and get a class label
            class_label = classify_image(filename)  # Implement this function

            return f'Image Class: {class_label}'

    return render_template('upload.html')


@app.route('/upload_cropped_image', methods=['POST'])
def upload_cropped_image():


     
    if 'croppedImage' in request.files:
        file = request.files['croppedImage']
        # Save the file
        file.save('uploads/image.png')
        return {'status': 'success'}
    else:
        return {'status': 'no file found'}, 400
    # TODO TRANSLATION LOGIC GOES HERE

    # STEP BY STEP#

    # 1. READ THE IMAGE

    # 2. CHECK THE LAGNUAGE? OR TRANSLATE THE TEXT

    # 3. CHECK THE TEXT WITH THE DATABASE (SUBSTRING MATCH?)


def classify_image(image_path):
    # Implement your image classification logic here
    # For now, returning a dummy class label
    return "Dummy Class"

if __name__ == '__main__':
    app.run(debug=True)