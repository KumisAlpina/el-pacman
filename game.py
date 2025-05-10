import pygame
from config import *
from sprites import *

class Game:
    def __init__(self):
        #iniciar pygame
        pygame.init()

        #iniciar la ventana
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("PAC-MAN")

        #Reloj velocidad del juego
        self.clock = pygame.time.Clock()

        #bucle principal
        self.running = True

        #crear el jugador
        self.player = Player()

    def handle_events(self):
        #manejar eventos
        for event in pygame.event.get():
            #si cierra la ventana
            if event.type == pygame.QUIT:
                self.running = False
   
    def update(self):
        #actualizar estado del juego
        #teclas presionadas
        keys = pygame.key.get_pressed()

        #calcular movimiento en base a las teclas presionadas
        dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]

        #mover el jugador
        self.player.move(dx, dy)

    def draw(self):
        #dibujar en la pantalla
       
        #llenando la pantalla de color negro
        self.screen.fill(BLACK)
       
        #dibujar el jugador
        self.player.draw(self.screen)
      
      #Actualizar la pantalla
        pygame.display.flip()

    def run(self):
        #bucle principal del juego
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)  # Limitar a 60 FPS