import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
import numpy as np
from PIL import Image
#import matplotlib.pyplot as plt
from torchvision import datasets, models, transforms
import time, copy

import os
from flask import Flask, session, flash, request, redirect, url_for, jsonify

from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/opt/data/img_uploads/'
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

            image = Image.open(r"/opt/data/img_uploads/"+filename)
            
            prediction = consume_model(image)

            if prediction == 0:
                diagnostic = {
                    "condition": "SIN PHYTOPTHORA",
                    "percentage": "0%",
                    "treatment": "<div><p>El control de esta enfermedad se basa en una combinación de medidas preventivas y curativas, incluyendo:</p><ol><li><p>Manejo adecuado del suelo: Es importante evitar el encharcamiento del suelo, mejorar la estructura del suelo y mantener una buena ventilación para reducir la propagación del hongo.</p></li><li><p>Control químico: Se pueden utilizar fungicidas para prevenir y tratar la infección por phytophthora palmivora. Es importante utilizar los fungicidas adecuados y seguir las instrucciones del fabricante para evitar problemas de resistencia o toxicidad.</p></li><li><p>Control biológico: La introducción de microorganismos benéficos que compiten con el hongo patógeno también puede ser efectivo. Por ejemplo, el uso de Trichoderma harzianum ha demostrado ser eficaz en la reducción de la infección por phytophthora en el cacao.</p></li><li><p>Podas y eliminación de plantas infectadas: Es importante eliminar las partes infectadas de la planta y, si es necesario, eliminar plantas enteras para prevenir la propagación del hongo.</p></li><li><p>Mejora de la resistencia de las plantas: La selección de variedades de cacao resistentes a phytophthora y la mejora de la salud general de las plantas a través de una nutrición adecuada y una gestión adecuada de plagas y enfermedades también pueden ayudar a prevenir la infección.</p></li></ol></div>"
                }
                return jsonify(diagnostic)
            elif prediction == 1:
                diagnostic = {
                    "condition": "LEVE",
                    "percentage": "0-5%",
                    "treatment": "<div><p>El control de esta enfermedad se basa en una combinación de medidas preventivas y curativas, incluyendo:</p><ol><li><p>Manejo adecuado del suelo: Es importante evitar el encharcamiento del suelo, mejorar la estructura del suelo y mantener una buena ventilación para reducir la propagación del hongo.</p></li><li><p>Control químico: Se pueden utilizar fungicidas para prevenir y tratar la infección por phytophthora palmivora. Es importante utilizar los fungicidas adecuados y seguir las instrucciones del fabricante para evitar problemas de resistencia o toxicidad.</p></li><li><p>Control biológico: La introducción de microorganismos benéficos que compiten con el hongo patógeno también puede ser efectivo. Por ejemplo, el uso de Trichoderma harzianum ha demostrado ser eficaz en la reducción de la infección por phytophthora en el cacao.</p></li><li><p>Podas y eliminación de plantas infectadas: Es importante eliminar las partes infectadas de la planta y, si es necesario, eliminar plantas enteras para prevenir la propagación del hongo.</p></li><li><p>Mejora de la resistencia de las plantas: La selección de variedades de cacao resistentes a phytophthora y la mejora de la salud general de las plantas a través de una nutrición adecuada y una gestión adecuada de plagas y enfermedades también pueden ayudar a prevenir la infección.</p></li></ol></div>"
                }
                return jsonify(diagnostic)
            elif prediction == 2:
                diagnostic = {
                    "condition": "MODERADO",
                    "percentage": "6-20%",
                    "treatment": "<div><p>El control de esta enfermedad se basa en una combinación de medidas preventivas y curativas, incluyendo:</p><ol><li><p>Manejo adecuado del suelo: Es importante evitar el encharcamiento del suelo, mejorar la estructura del suelo y mantener una buena ventilación para reducir la propagación del hongo.</p></li><li><p>Control químico: Se pueden utilizar fungicidas para prevenir y tratar la infección por phytophthora palmivora. Es importante utilizar los fungicidas adecuados y seguir las instrucciones del fabricante para evitar problemas de resistencia o toxicidad.</p></li><li><p>Control biológico: La introducción de microorganismos benéficos que compiten con el hongo patógeno también puede ser efectivo. Por ejemplo, el uso de Trichoderma harzianum ha demostrado ser eficaz en la reducción de la infección por phytophthora en el cacao.</p></li><li><p>Podas y eliminación de plantas infectadas: Es importante eliminar las partes infectadas de la planta y, si es necesario, eliminar plantas enteras para prevenir la propagación del hongo.</p></li><li><p>Mejora de la resistencia de las plantas: La selección de variedades de cacao resistentes a phytophthora y la mejora de la salud general de las plantas a través de una nutrición adecuada y una gestión adecuada de plagas y enfermedades también pueden ayudar a prevenir la infección.</p></li></ol></div>"
                }
                return jsonify(diagnostic)
            elif prediction == 3:
                diagnostic = {
                    "condition": "SEVERO",
                    "percentage": "20% a más",
                    "treatment": "<div><p>El control de esta enfermedad se basa en una combinación de medidas preventivas y curativas, incluyendo:</p><ol><li><p>Manejo adecuado del suelo: Es importante evitar el encharcamiento del suelo, mejorar la estructura del suelo y mantener una buena ventilación para reducir la propagación del hongo.</p></li><li><p>Control químico: Se pueden utilizar fungicidas para prevenir y tratar la infección por phytophthora palmivora. Es importante utilizar los fungicidas adecuados y seguir las instrucciones del fabricante para evitar problemas de resistencia o toxicidad.</p></li><li><p>Control biológico: La introducción de microorganismos benéficos que compiten con el hongo patógeno también puede ser efectivo. Por ejemplo, el uso de Trichoderma harzianum ha demostrado ser eficaz en la reducción de la infección por phytophthora en el cacao.</p></li><li><p>Podas y eliminación de plantas infectadas: Es importante eliminar las partes infectadas de la planta y, si es necesario, eliminar plantas enteras para prevenir la propagación del hongo.</p></li><li><p>Mejora de la resistencia de las plantas: La selección de variedades de cacao resistentes a phytophthora y la mejora de la salud general de las plantas a través de una nutrición adecuada y una gestión adecuada de plagas y enfermedades también pueden ayudar a prevenir la infección.</p></li></ol></div>"
                }
                return jsonify(diagnostic)
            else:
                diagnostic = {
                    "condition": "-",
                    "percentage": "-",
                    "treatment": "<div><p>El control de esta enfermedad se basa en una combinación de medidas preventivas y curativas, incluyendo:</p><ol><li><p>Manejo adecuado del suelo: Es importante evitar el encharcamiento del suelo, mejorar la estructura del suelo y mantener una buena ventilación para reducir la propagación del hongo.</p></li><li><p>Control químico: Se pueden utilizar fungicidas para prevenir y tratar la infección por phytophthora palmivora. Es importante utilizar los fungicidas adecuados y seguir las instrucciones del fabricante para evitar problemas de resistencia o toxicidad.</p></li><li><p>Control biológico: La introducción de microorganismos benéficos que compiten con el hongo patógeno también puede ser efectivo. Por ejemplo, el uso de Trichoderma harzianum ha demostrado ser eficaz en la reducción de la infección por phytophthora en el cacao.</p></li><li><p>Podas y eliminación de plantas infectadas: Es importante eliminar las partes infectadas de la planta y, si es necesario, eliminar plantas enteras para prevenir la propagación del hongo.</p></li><li><p>Mejora de la resistencia de las plantas: La selección de variedades de cacao resistentes a phytophthora y la mejora de la salud general de las plantas a través de una nutrición adecuada y una gestión adecuada de plagas y enfermedades también pueden ayudar a prevenir la infección.</p></li></ol></div>"
                }
                return jsonify(diagnostic)

            #return jsonify(diagnostic)
    else:
        return jsonify({'message': 'Metodo no soportado.'})

def predict(model, img):
  prediction = None
  model.eval()
  with torch.no_grad():
    output= model(img)
    prediction= torch.argmax(output).item()
  return prediction

transform=transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms. ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                          [0.229, 0.224, 0.225])
])

def consume_model(img):

  device =('cpu')
  model_ft = models.resnet18(weights='ResNet18_Weights.DEFAULT')
  num_ft = model_ft.fc.in_features
  model_ft.fc = nn.Linear(num_ft, 4)
  model_ft = model_ft.to(device)

  model_ft.load_state_dict(torch.load("trained_model_ft.pth"))
  model_ft.eval()
  
  image = transform(img).unsqueeze(0)
  prediction = predict(model_ft, image)

  return prediction

if __name__ == '__main__' :
    app.run(host="0.0.0.0", debug=True, port=4000)