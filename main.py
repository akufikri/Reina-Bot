from flask import Flask, request, render_template, redirect, url_for, send_from_directory
from rembg import remove
from PIL import Image
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'in'
OUTPUT_FOLDER = 'out'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/edit/<filename>')
def edit_file(filename):
    return render_template('edit.html', filename=filename)

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'files[]' not in request.files:
        return redirect(url_for('index'))
    
    files = request.files.getlist('files[]')

    output_files = []

    for file in files:
        if file.filename == '':
            continue

        input_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(input_path)

        with open(input_path, 'rb') as input_file:
            input_image = Image.open(input_file)
            output_image = remove(input_image)

        output_path = os.path.join(OUTPUT_FOLDER, file.filename)
        output_image.save(output_path, format='PNG')
        output_files.append(file.filename)

    return render_template('result.html', output_files=output_files)

@app.route('/out/<filename>')
def get_result(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
