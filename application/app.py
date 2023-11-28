from flask import Flask, request, render_template, redirect, url_for
import os
from PIL import Image
from googletrans import Translator
import pytesseract

app = Flask(__name__)

# Ensure there is a folder named 'uploads' in the same directory as this script
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
translate_result = []

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


@app.route('/upload_cropped_image', methods=['GET','POST'])
def upload_cropped_image():
    if request.method == 'POST':
        if 'croppedImage' in request.files:
            empty_flag = 0
            file = request.files['croppedImage']
            # Save the file
            file.save('uploads/image.png')


            # Path to your Tesseract executable (if not in PATH)
            pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

            # Load an image
            image_path = 'uploads/image.png'
            image = Image.open(image_path)

            # Perform OCR on the image
            extracted_text = pytesseract.image_to_string(image, lang='eng+jpn')

            # Initialize the translator
            translator = Translator()
            try:
            # Translate the extracted text to Japanese
                translated_text = translator.translate(extracted_text, src='ja', dest='en')

                print("Original Text:")
                print(extracted_text)

                print("\nTranslated Text:")
                print(translated_text.text)
                translate_result.append(translated_text.text)
            except:
                print("Empty Text Found")
                empty_flag = 1

        else:
            return {'status': 'no file found'}, 400
    

    return render_template('result.html')
                           #, class_label=translated_text.text)


@app.route('/result')
def result():
    return render_template('result.html', info=translate_result)


def classify_image(image_path):
    # Implement your image classification logic here
    # For now, returning a dummy class label
    return "Dummy Class"

if __name__ == '__main__':
    app.run(debug=True)