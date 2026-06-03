# mapping/occupancy_grid.py

import numpy as np
import cv2 as cv

XY_RESOLUTION = 0.2

X_MIN = -5
X_MAX = 5

Y_MIN = -5
Y_MAX = 5

robot_path = []

# branco
grid_map = np.ones(
    (
        int((X_MAX - X_MIN) / XY_RESOLUTION),
        int((Y_MAX - Y_MIN) / XY_RESOLUTION),
        3
    ),
    dtype=np.uint8
) * 255

# Teste do plot do mapa (deixa ele todo cinza com um quadrado branco)
##grid_map[:, :] = 100
##grid_map[10:20, 10:20] = 255

# paredes (igual ao script do professor)
grid_map[0:int(0.15/XY_RESOLUTION)+1, :] = 255

grid_map[
    int((10/XY_RESOLUTION))-int(0.15/XY_RESOLUTION)-1:
    int((10/XY_RESOLUTION)),
    :
] = 255

grid_map[:, 0:1] = 255

grid_map[
    :,
    int((10/XY_RESOLUTION))-int(0.15/XY_RESOLUTION)-1:
    int((10/XY_RESOLUTION))
] = 255


def convert_to_map(position):

    pos_x = (
        int(position[0] / XY_RESOLUTION)
        + int(((Y_MAX - Y_MIN) / XY_RESOLUTION) / 2)
    )

    pos_y = (
        int(position[1] / XY_RESOLUTION)
        + int(((Y_MAX - Y_MIN) / XY_RESOLUTION) / 2)
    )

    return [pos_x, pos_y]


def add_cone(position):

    map_position = convert_to_map(position)

    print(
        "Posição mundo:",
        position,
        "-> mapa:",
        map_position
    )

    if (
        0 <= map_position[0] < grid_map.shape[0]
        and
        0 <= map_position[1] < grid_map.shape[1]
    ):

        #print("MARCANDO CONE")

        # marca cone
        grid_map[
            map_position[0],
            map_position[1]
        ] = [0, 0, 255]

def add_robot_path(position):

    map_position = convert_to_map(position)

    if (
        0 <= map_position[0] < grid_map.shape[0]
        and
        0 <= map_position[1] < grid_map.shape[1]
    ):

        current = grid_map[
            map_position[0],
            map_position[1]
        ]

        # não sobrescrever cone vermelho
        if not np.array_equal(
            current,
            [0, 0, 255]
        ):
            grid_map[
                map_position[0],
                map_position[1]
            ] = [0, 0, 0]

def get_map():
    return grid_map