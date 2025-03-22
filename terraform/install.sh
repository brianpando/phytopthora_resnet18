#!/bin/bash
set -e

#apt update && apt upgrade -y
apt install -y python3 python3-pip python3-venv git

# Clonar tu repositorio
git clone https://github.com/brianpando/phytopthora_resnet18.git

mkdir -p /opt/data/img_uploads
cd /home/root/phytopthora_resnet18
python3 -m venv venv
source venv/bin/activate

# Instalar Flask y Torch
pip install flask torch torchvision gunicorn

# Iniciar la aplicación con Gunicorn
gunicorn --bind 0.0.0.0:5000 main:app --daemon
