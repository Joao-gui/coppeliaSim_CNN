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

        # resolution[1] = Altura, resolution[0] = Largura, 3 = Canais de cores
        image = image.reshape(resolution[1], resolution[0], 3)

        # Corrige a orientação da imagem, Coppelia envia aa imagem de ponta cabeça
        image = cv.flip(image, 0)

        # Correção de cores, Coppelia trabalha com imagem BRG não RGB
        image = cv.cvtColor(image, cv.COLOR_RGB2BGR)

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
            # Tamanho da fonte (0.5=pequena, 1.0=grande, 2.0=enorme)
            0.75,
            # Cor do texto BGR
            (0, 255, 0),
            # Espessura da letra (1-fina, 2-média, 3-grossa)
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