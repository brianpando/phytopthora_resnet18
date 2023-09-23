import os
from flask import Flask, session, flash, request, redirect, url_for, jsonify

from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/phytopthora/opt/img_uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.secret_key = "super secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from diagnostic import diagnostic


@app.route('/verificacion', methods=['GET'])
def verify():
    return jsonify({'message': 'hola'})


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/diagnosticar', methods=['POST', 'GET'])
def to_diagnose():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return jsonify({'message': 'No file.'})
            #return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            #return jsonify(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #return redirect(url_for('download_file', name=filename))
        
        return jsonify(diagnostic)
    else:
        return jsonify({'message': 'Metodo no soportado.'})


if __name__ == '__main__' :
    app.run(host="0.0.0.0", debug=True, port=4000)