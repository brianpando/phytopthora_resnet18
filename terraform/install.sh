#!/bin/bash
set -e

apt update && apt upgrade -y
apt install -y python3 python3-pip python3-venv git

mkdir -p /home/root/cacao_flask_app
cd /home/root/cacao_flask_app
python3 -m venv venv
source venv/bin/activate

# Instalar Flask y Torch
pip install flask torch torchvision gunicorn

# Clonar tu repositorio
git clone https://github.com/brianpando/phytopthora_resnet18.git /home/root/cacao_flask_app

# Iniciar la aplicación con Gunicorn
gunicorn --bind 0.0.0.0:5000 main:app --daemon
