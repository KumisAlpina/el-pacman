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
        self.walls = []
        self.player = None
        self.create_level()

    def create_level(self):
        """Crear el nivel a partir de la matriz LEVEL"""
        for row_index, row in enumerate(LEVEL):
            for col_index, cell in enumerate(row):
                if cell == "1":
                    # Crear una pared
                    self.walls.append(Wall(col_index, row_index))
                elif cell == "P":
                    self.player = Player(col_index, row_index)

    def handle_events(self):
        #manejar eventos
        for event in pygame.event.get():
            #si cierra la ventana
            if event.type == pygame.QUIT:
                self.running = False
   
    def update(self):
        #actualizar estado del juego
        #mover el jugador
        self.player.update(self.walls)

    def draw(self):
        #dibujar en la pantalla
       
        #llenando la pantalla de color negro
        self.screen.fill(BLACK)

        #dibujar paredes
        for wall in self.walls:
            wall.draw(self.screen)
       
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