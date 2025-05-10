import pygame
from config import *

class Player:
    def __init__(self):
        #pocicion inicial al centro de la pantalla
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2

        #cargar sprite de Pacman
        self.sprite_sheet = load_image("pacman.png")

        #obtener imagen de pacman
        self.origin_image = pygame.Surface((16, 16), pygame.SRCALPHA)
        self.origin_image.blit(self.sprite_sheet, (0, 0), (0, 0, 16, 16))
        self.origin_image = pygame.transform.scale(self.origin_image, (PLAYER_SIZE, PLAYER_SIZE))

        #imagen actual del jugador
        self.image = self.origin_image

        #crear rectangulo para coliciones y posicionamiento
        self.rect = self.image.get_rect(center=(self.x, self.y))

        #Direccion actual(0: derecha, 1: izquierda)
        self.direction = 0
        self.flipped = False

    
    def move(self, dx, dy):
        #mover el jugador
        self.x += dx * PLAYER_SPEED
        self.y += dy * PLAYER_SPEED
        
        #Mantener el jugador dentro de la pantalla
        if self.x > SCREEN_WIDTH - PLAYER_SIZE:
            self.x = 0
        elif self.x < 0:
            self.x = SCREEN_WIDTH - PLAYER_SIZE
        
        if self.y > SCREEN_HEIGHT - PLAYER_SIZE:
            self.y = 0
        elif self.y < 0:
            self.y = SCREEN_HEIGHT - PLAYER_SIZE
        
        #actualizar el rectangulo
        self.rect.center = (self.x, self.y)

        #actualizar la direccion
        if dx > 0 and self.direction != 0:
            self.direction = 0 #derecha
            self.image = self.origin_image
            self.flipped = False

        elif dx < 0 and self.direction != 1:
            self.direction = 1 #izquierda
            self.image = pygame.transform.flip(self.image, True, False)
            self.flipped = True

        
    
    def draw(self, screen):
        #dibujar el jugador
        screen.blit(self.image, self.rect)