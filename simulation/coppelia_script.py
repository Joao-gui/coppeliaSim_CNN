import cv2 as cv
import numpy as np

from vision.inference import predict_image
from time import sleep
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

from mapping.occupancy_grid import add_cone, get_map, add_robot_path

# Cliente simulador
#print("Iniciando conexão")
client = RemoteAPIClient()
#print("Obtendo sim")
sim = client.require('sim')

# Objetos do modelo
#print("Obtendo handles")
sensor1Handle = sim.getObject('/Vision_sensor')
robotHandle = sim.getObject('/PioneerP3DX')
maskSensorHandle = sim.getObject('/mask')

# Stepping mode
sim.setStepping(True)

# Inicio Simulação
#print("Iniciando simulação")
sim.startSimulation()

# Nao repete pontos
last_mark_time = 0

# offset para distanciar cones do robo
offset = 0.30 # distância
angle_offset = -0.2 # radianos

try:

    while (t := sim.getSimulationTime()) < 30:
        #print("Loop")
        # capturar imagem
        buf, resolution = sim.getVisionSensorImg(sensor1Handle)

        image = np.frombuffer(buf, dtype=np.uint8)

        # resolution[1] = Altura, resolution[0] = Largura, 3 = Canais de cores
        image = image.reshape(resolution[1], resolution[0], 3)

        # Corrige a orientação da imagem, Coppelia envia aa imagem de ponta cabeça
        image = cv.flip(image, 0)

        # Correção de cores, Coppelia trabalha com imagem BGR não RGB
        image = cv.cvtColor(image, cv.COLOR_RGB2BGR)

        # IA
        classe, confidence = predict_image(image)

        # mostrar no terminal
        #print(f'Classe: {classe}')

        # desenhar texto
        display = image.copy()

        # Sensor mask
        buf_mask, resolution_mask = sim.getVisionSensorImg(maskSensorHandle)

        mask = np.frombuffer(buf_mask, dtype=np.uint8)

        mask = mask.reshape(resolution_mask[1],resolution_mask[0],3)

        mask = cv.flip(mask, 0)

        # Converte para escala de cinza
        mask_gray = cv.cvtColor(mask,cv.COLOR_BGR2GRAY)

        # Contar pixels brancos
        white_pixels = cv.countNonZero(mask_gray)

        # print para mostrar quantidade de pixels se o objeto esta perto ou lonje (quanto maior mais perto)
        #print("Pixels brancos:", white_pixels)

        # Detectando cone e salvando posição
        if classe == "RED_CONE" and confidence < 0.10 and (t - last_mark_time) > 2 and white_pixels > 2350:
            #robot_pos = sim.getObjectPosition(robotHandle, -1)
            #add_cone(robot_pos)
            robot_pos = sim.getObjectPosition(robotHandle, -1)
            robot_ori = sim.getObjectOrientation(robotHandle, -1)

            yaw = robot_ori[2]

            cone_pos = [
                robot_pos[0] + offset * np.cos(yaw + angle_offset),
                robot_pos[1] + offset * np.sin(yaw + angle_offset),
                robot_pos[2]
            ]

            add_cone(cone_pos)
            
            last_mark_time = t
            print(f"CONE DETECTADO | "f"Posição: {robot_pos}")

        # Caminho robo
        robot_pos = sim.getObjectPosition(robotHandle, -1)

        add_robot_path(robot_pos)

        # Mostre no mapa
        map_display = get_map().copy()

        map_display = cv.resize(map_display, (600,600), interpolation=cv.INTER_NEAREST)

        cell_size = 12
        
        for x in range(0, 600, cell_size):
            cv.line(
                map_display,
                (x, 0),
                (x, 600),
                (0, 0, 0),
                1
            )

        for y in range(0, 600, cell_size):
            cv.line(
                map_display,
                (0, y),
                (600, y),
                (0, 0, 0),
                1
            )

        cv.imshow("Mapa de Cones", map_display)

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