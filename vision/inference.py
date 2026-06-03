import cv2
import numpy as  np
import tensorflow as tf

from tensorflow.keras.models import load_model

# carregar modelo uma vez
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / 'models' / 'mobilenet_model.h5'

model = load_model(MODEL_PATH)

# labels
classes = ['RED_CONE', 'RED_CUBE']

def predict_image(img):

    # resize (244,244)
    img = cv2.resize(img, (224,224))

    # preprocessamento MobileNet
    img = tf.keras.applications.mobilenet_v2.preprocess_input(img)

    # batch dimension
    img = np.expand_dims(img, axis=0)

    # predição
    prediction = model.predict(img, verbose=0)

    valor = float(prediction[0][0])

    #print(f"Valor bruto da rede: {valor}")

    # converter para classe, transforma número da IA em texto prediction[0][0] é um numero de 0 a 1
    classe = classes[int(valor > 0.5)]

    # confiança
    confidence = valor

    return classe, confidence