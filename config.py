import pygame
import os

#CONFIGURACIONES DE LA VENTANA

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#CONFIGURACIONES DEL JUGADOR
PLAYER_SIZE = 23
PLAYER_SPEED = 2
ANIMATION_SPEED = 50
ANIMATION_FRAMES = 8

#CONFIGURACION DE LOS FANTASMAS
GHOST_SIZE = 30
GHOST_ANIMATION_FRAMES = 8
GHOST_ANIMATION_SPEED = 150

#velocidades de los fantasmas
GHOST_SPEEDS = {
    'red': 3,
    'blue': 2,
    'orange':2,
    'green': 1
}

#tiempos de direccion
GHOST_DIRECTION_TIMES = {
    'red': 2000,
    'blue': 2000,
    'orange':2000,
    'green': 2000
}

#nombres de los fantasmas
GHOST_SPRITES = {
    'red': 'redGhost.png',
    'blue': 'blueGhost.png',
    'orange': 'orangeGhost.png',
    'green': 'greenGhost.png'
}

#CONFIGURACION DE LAS PAREDES
TILE_SIZE = 32
WALL_COLOR = (33, 33, 255)

#CONFIGURACION DE MONEDAS
COIN_SIZE = 15
COIN_ANIMATION_SPEED = 200
COIN_FRAMES = 8
POINTS_PER_COIN = 10

#CONFIGURACION DE LAS COLICIONES
COLLISION_TOLERANCE = 4
SLIDE_SPEED = 1

# ESTADOS DEL JUEGO
PLAYING = 'playing'
GAME_OVER = 'game_over'

#DIRECCIONES
RIGHT = 0
LEFT = 1
UP = 2
DOWN = 3

#COLORES
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

#LEVELS
LEVEL = [
    "1111111111111111111111111",
    "1R000000000010000000000B1",
    "1011101111101011111011101",
    "1011101111101011111011101",
    "1000000000000000000000001",
    "1011101011111111101011101",
    "1000001000001000001000001",
    "1111101111101011111011111",
    "1111101000000000001011111",
    "0000000011111111100000000",
    "1111101000000000001011111",
    "1000001011111111101000001",
    "1011101011111111101011101",
    "100010000000P000000010001",
    "1110101011111111101010111",
    "10000010000010000010000G1",
    "1011111111101011111111101",
    "1O00000000000000000000001",
    "1111111111111111111111111"
]

#FUNCION PARA CARGAR IMAGENES
def load_image(name):
    return pygame.image.load(os.path.join("assets", name)).convert_alpha()