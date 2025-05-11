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
        self.game_state = PLAYING

        #crear el jugador, paredes y monedas(fantasmas)
        self.walls = []
        self.coins = []
        self.score = 0
        self.player = None
        self.ghosts = []
        self.create_level()

        #Fuente para el texto
        self.font = pygame.font.Font(None, 36)

    def create_level(self):
        """Crear el nivel a partir de la matriz LEVEL"""
        for row_index, row in enumerate(LEVEL):
            for col_index, cell in enumerate(row):
                if cell == "1":
                    # Crear una pared
                    self.walls.append(Wall(col_index, row_index))
                elif cell == "0":
                    self.coins.append(Coin(col_index, row_index))
                elif cell == "P":
                    self.player = Player(col_index, row_index)
                elif cell == "R":
                    self.ghosts.append(Ghost(col_index, row_index, 'red'))
                elif cell == "B":
                    self.ghosts.append(Ghost(col_index, row_index, 'blue'))
                elif cell == "O":
                    self.ghosts.append(Ghost(col_index, row_index, 'orange'))
                elif cell == "G":
                    self.ghosts.append(Ghost(col_index, row_index, 'green'))

    def handle_events(self):
        #manejar eventos
        for event in pygame.event.get():
            #si cierra la ventana
            if event.type == pygame.QUIT:
                self.running = False
        if self.game_state == GAME_OVER:
            self.running = False
   
    def update(self):
        #actualizar estado del juego
        #mover el jugador
        if self.game_state == PLAYING:
            self.player.update(self.walls)

            #actualizar fantasmas
            for ghost in self.ghosts:
                ghost.update(self.walls)
                if self.player.rect.colliderect(ghost.rect):
                    self.game_state = GAME_OVER

        #actualizar monedas y comprobar coliciones
        for coin in self.coins[:]: #usar una copia de la lista para modificarla
            coin.update()
            if self.player.rect.colliderect(coin.rect):
                self.coins.remove(coin)
                self.score += POINTS_PER_COIN

        

    def draw(self):
        #dibujar en la pantalla
       
        #llenando la pantalla de color negro
        self.screen.fill(BLACK)

        #dibujar paredes
        for wall in self.walls:
            wall.draw(self.screen)
        
        #dibujar las monedas
        for coin in self.coins:
            coin.draw(self.screen)
       
        #dibujar el jugador
        self.player.draw(self.screen)
        
        for ghost in self.ghosts:
            ghost.draw(self.screen)

        #dibujar el puntaje
        score_text = self.font.render(f'Puntaje: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        #Actualizar la pantalla
        pygame.display.flip()

    def run(self):
        #bucle principal del juego
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)  # Limitar a 60 FPS