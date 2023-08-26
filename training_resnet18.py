import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision
import numpy as np
#import matplotlib.pyplot as plt
from torchvision import datasets, models, transforms
import time
import copy

def train_model(model, criterio, optimizer, scheduler, num_epochs = 25):
  since = time.time()
  best_model_wts = copy.deepcopy(model.state_dict())
  best_acc = 0.0
  for epoch in range(num_epochs):
    #print('Epoch {}/{}'.format(epoch, num_epochs-1))
    #Train model
    #scheduler.step()
    model.train()
    running_loss = 0.0
    running_corrects = 0.0
    
    for inputs, labels in train_loader:
        inputs = inputs.to(device)
        labels = labels.to(device)
        optimizer.zero_grad()
        
        outputs = model(inputs)
        _, preds = torch.max(outputs, 1)
        loss = criterion(outputs, labels)
          
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item() * inputs.size(0)
        running_corrects += torch.sum(preds == labels.data)
    scheduler.step()
    epoch_loss = running_loss /len(train_dataset)
    epoch_acc = running_corrects.double() / len(train_dataset)
    #print('Train Loss: {:.4f} Acc: {:.4f}'.format(epoch_loss, epoch_acc))
    #Validation 
    model.eval()
    running_loss = 0.0
    running_corrects = 0.0
    
    for inputs, labels in test_loader:
      inputs = inputs.to(device)
      labels = labels.to(device)
        
      with torch.set_grad_enabled(False):
        outputs = model(inputs)
        _, preds = torch.max(outputs, 1)
        loss = criterion(outputs, labels)
          
      running_loss += loss.item() * inputs.size(0)
      running_corrects += torch.sum(preds == labels.data)
     
    epoch_loss = running_loss /len(test_dataset)
    epoch_acc = running_corrects.double() / len(test_dataset)
      
    #print('Val Loss: {:.4f} Acc: {:.4f}'.format(epoch_loss, epoch_acc))
    if epoch_acc > best_acc:
        best_acc = epoch_acc
        best_model_wts = copy.deepcopy(model.state_dict())
        
  time_elapsed = time.time() - since
  #print('Training complete in {:.0f}m {:.0f}s'.format(time_elapsed//60, time_elapsed % 60))
  #print('Best val accucary: {:.4f}'.format(best_acc))
  model.load_state_dict(best_model_wts)
  return model

#----------------------------
print("INICIANDO FITOFTORA") 

train_dataset = torchvision.datasets.ImageFolder('phytopthora_data/train',
                                                transform=transforms.Compose([
                                                    transforms.RandomResizedCrop(224),
                                                    transforms. ToTensor(),
                                                    transforms.Normalize([0.485, 0.456, 0.406],
                                                                         [0.229, 0.224, 0.225])
                                                    
                                                ]))
#recibir 1 imagen y guardarlo en la carpeta phytopthora_data/val
test_dataset = torchvision.datasets.ImageFolder('phytopthora_data/val',
                                              transform=transforms.Compose([
                                                    transforms.Resize(256),
                                                    transforms.CenterCrop(224),
                                                    transforms. ToTensor(),
                                                    transforms.Normalize([0.485, 0.456, 0.406],
                                                                         [0.229, 0.224, 0.225])
                                                ]))
#print(test_dataset)
train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=4, shuffle=True)
test_loader= torch.utils.data.DataLoader(test_dataset, batch_size=4, shuffle=True)

class_names = train_dataset.classes
  
inputs, classes = next(iter(train_loader))
out = torchvision.utils.make_grid(inputs)
#imshow(out, title=[class_names[x] for x in classes]) #muestra las imagenes del dataset
#device = ('cuda' if torch.cuda.is_available() else 'cpu')
device =('cpu')
#-----------------------
#model_ft = models.resnet18(pretrained=True) #warning use weigths
model_ft = models.resnet18(weights='ResNet18_Weights.DEFAULT')
num_ft = model_ft.fc.in_features

model_ft.fc = nn.Linear(num_ft, 2)

model_ft = model_ft.to(device)
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model_ft.parameters(), lr=0.001, momentum=0.9)
scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=7, gamma=0.1)
print("training...")
model_ft = train_model(model_ft, criterion, optimizer, scheduler, num_epochs=25)
print("trained")

torch.save(model_ft.state_dict(),"trained_resenet18.pth")

#python main_resnet18.py