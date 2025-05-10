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
        self.image = pygame.Surface((16, 16), pygame.SRCALPHA)
        self.image.blit(self.sprite_sheet, (0, 0), (0, 0, 16, 16))
        self.image = pygame.transform.scale(self.image, (PLAYER_SIZE, PLAYER_SIZE))

        #crear rectangulo para coliciones y posicionamiento
        self.rect = self.image.get_rect(center=(self.x, self.y))

    
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
    
    def draw(self, screen):
        #dibujar el jugador
        screen.blit(self.image, self.rect)