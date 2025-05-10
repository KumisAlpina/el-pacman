import pygame
from config import *

class Player:
    def __init__(self):
        #pocicion inicial al centro de la pantalla
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2

        #cargar sprite de Pacman
        self.sprite_sheet = load_image("PacMan.png")

        #cargar todos los sprites
        self.animation_frames = []
        for i in range(ANIMATION_FRAMES):
            #crear superficie para cada sprite
            frame = pygame.Surface((16, 16), pygame.SRCALPHA)
            #copiar el frame del sprite sheet
            frame.blit(self.sprite_sheet, (0, 0), (i * 16, 0, 16, 16))
            #escalar el frame a el tamaño del jugador
            frame = pygame.transform.scale(frame, (PLAYER_SIZE, PLAYER_SIZE))
            self.animation_frames.append(frame)
        #variables para la animacion
        self.current_frame = 0
        self.animation_timer = pygame.time.get_ticks()
        self.is_moving = False

        #imagen actual del jugador
        self.original_image = self.animation_frames[0]
        self.image = self.original_image

        #crear rectangulo para coliciones y posicionamiento
        self.rect = self.image.get_rect(center=(self.x, self.y))

        #Direccion actual
        self.direction = RIGHT

        #deltas
        self.dx = 0
        self.dy = 0 

    def update_animation(self):
        #actualizar frame de la animacion
        if not self.is_moving:
            self.current_frame = 0
            return
        
        current_time = pygame.time.get_ticks()

        if current_time - self.animation_timer > ANIMATION_SPEED:
            self.current_frame = (self.current_frame + 1) % ANIMATION_FRAMES
            self.animation_timer = current_time
    
    def update_image(self):
        #actualizar la imagen segun la direccion y el frame actual
        self.original_image = self.animation_frames[self.current_frame]


        #actualizar la direccion
        if self.dx > 0:
            self.direction = RIGHT #derecha
            self.image = self.original_image

        elif self.dx < 0:
            self.direction = LEFT #izquierda
            self.image = pygame.transform.flip(self.original_image, True, False)
            
        elif self.dy < 0:
            self.direction = UP  #arriba
            self.image = pygame.transform.rotate(self.original_image, 90)
           
        elif self.dy > 0:
            self.direction = DOWN #abajo
            self.image = pygame.transform.rotate(self.original_image, -90)
            

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
        self.dx = dx
        self.dy = dy

        #actualizar estado del movimiento
        self.is_moving = dx != 0 or dy != 0

    def update(self):
        #actualizar la animacion
        self.update_animation()

        #actualizar la imagen
        self.update_image()

        

        
    
    def draw(self, screen):
        #dibujar el jugador
        screen.blit(self.image, self.rect)