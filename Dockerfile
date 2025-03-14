FROM python:3.9
WORKDIR /app
COPY app/ /app/
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /opt/data/train /opt/data/test /opt/img_uploads && \
    chmod -R 777 /opt/data/

# Entrena el modelo si no existe
RUN if [ ! -f "/app/model.pth" ]; then python training_resnet18.py; fi

# Expone el puerto en el que corre Flask
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "main.py"]
