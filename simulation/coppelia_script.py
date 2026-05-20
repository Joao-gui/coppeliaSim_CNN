import cv2 as cv
import numpy as np

from vision.inference import predict_image
from time import sleep
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

# Cliente simulador
client = RemoteAPIClient()
sim = client.require('sim')

# Objetos do modelo
sensor1Handle = sim.getObject('/Vision_sensor')
robotHandle = sim.getObject('/PioneerP3DX')

# Stepping mode
sim.setStepping(True)

# Inicio Simulação
sim.startSimulation()

try:

    while (t := sim.getSimulationTime()) < 30:

        # capturar imagem
        buf, resolution = sim.getVisionSensorImg(sensor1Handle)

        image = np.frombuffer(buf, dtype=np.uint8)

        image = image.reshape(resolution[1], resolution[0], 3)

        image = cv.flip(image, 0)

        # IA
        classe, confidence = predict_image(image)

        # mostrar no terminal
        #print(f'Classe: {classe}')

        # desenhar texto
        display = image.copy()

        cv.putText(
            display,
            f'{classe} ({confidence:.2f})',
            # Posição da fonte
            (5, 40),
            cv.FONT_HERSHEY_SIMPLEX,
            # Tamanho da fonte
            0.75,
            (0, 255, 0),
            2
        )

        # exibir câmera
        cv.imshow('Camera Frontal', display)

        # tecla
        key = cv.waitKey(1)

        # apertar Q para sair
        if key == ord('q'):
            break

        # próximo step
        sim.step()

finally:

    # encerrar simulação
    sim.stopSimulation()

    # fechar janelas OpenCV
    cv.destroyAllWindows()