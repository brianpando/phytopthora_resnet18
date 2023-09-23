import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
import numpy as np
from PIL import Image
#import matplotlib.pyplot as plt
from torchvision import datasets, models, transforms
import time
import copy

def predict(model, img):
  prediction = None
  model.eval()
  with torch.no_grad():
    output= model(img)
    prediction= torch.argmax(output).item()
  return prediction
#----------------------------

transform=transforms.Compose([
    transforms.RandomResizedCrop(224),
    transforms. ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                          [0.229, 0.224, 0.225])
    
])
print("INICIANDO FITOFTORA") 

#imshow(out, title=[class_names[x] for x in classes]) #muestra las imagenes del dataset
#device = ('cuda' if torch.cuda.is_available() else 'cpu')
device =('cpu')
#-----------------------
#model_ft = models.resnet18(pretrained=True) #warning use weigths
model_ft = models.resnet18(weights='ResNet18_Weights.DEFAULT')
num_ft = model_ft.fc.in_features

model_ft.fc = nn.Linear(num_ft, 4)

model_ft = model_ft.to(device)
print("loading model from file...")
model_ft.load_state_dict(torch.load("trained_model_ft.pth"))
model_ft.eval()
print("loaded")
image = Image.open(r"image4.jpg")
image = transform(image).unsqueeze(0)
prediction=predict(model_ft, image)
print("result")
print(prediction)

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