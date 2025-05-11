import pygame, sys
from config import *
from sprites import *
from button import Button


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

        # Sonidos
        self.default_sound = pygame.mixer.Sound("assets/default.wav")
        self.pellet1_sound = pygame.mixer.Sound("assets/pellet1.wav")
        self.pellet2_sound = pygame.mixer.Sound("assets/pellet2.wav")
        self.levelintro_sound = pygame.mixer.Sound("assets/levelintro.wav")
        self.death_sound = pygame.mixer.Sound("assets/death.wav")
        self.default_channel = None
        self.pellet_toggle = True  # Para alternar entre pellet1 y pellet2

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
                pygame.quit()
                sys.exit()
            if self.game_state == GAME_OVER:
                 self.restart()



    def restart(self):
        show_restart = True
        screen_width = SCREEN_WIDTH
        screen = self.screen
        clock = self.clock

        def get_font(size):
            return pygame.font.Font(None, size)

        while show_restart:
            mouse_pos = pygame.mouse.get_pos()
            screen.fill("black")

            gameover_text = get_font(75).render("GAME OVER", True, "red")
            gameover_rect = gameover_text.get_rect(center=(screen_width // 2, 260))
            screen.blit(gameover_text, gameover_rect)

            back_button = Button(
                pos=(screen_width // 2, 460),
                text_input="VOLVER",
                font=get_font(45),
                base_color="White",
                hovering_color="Green"
            )

            back_button.changeColor(mouse_pos)
            back_button.update(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button.checkForInput(mouse_pos):
                        show_restart = False
                        # Esto es una muy mala práctica, pero lo dejo aquí para que funcione
                        import main
                        main.main_menu()
            pygame.display.update()
            clock.tick(60)


   
    def update(self):
        #actualizar estado del juego
        #mover el jugador
        if self.game_state == PLAYING:
            self.player.update(self.walls)

            #actualizar fantasmas
            for ghost in self.ghosts:
                ghost.update(self.walls)
                if self.player.rect.colliderect(ghost.rect):
                    # Detener cualquier sonido de fondo
                    if self.default_channel:
                        self.default_channel.stop()
                    # Sonar death.wav
                    self.death_sound.play()
                    # Esperar a que termine death.wav antes de pasar a GAME_OVER
                    while pygame.mixer.get_busy():
                        pygame.time.delay(10)
                    self.game_state = GAME_OVER

        #actualizar monedas y comprobar coliciones
        for coin in self.coins[:]: #usar una copia de la lista para modificarla
            coin.update()
            if self.player.rect.colliderect(coin.rect):
                self.coins.remove(coin)
                self.score += POINTS_PER_COIN
                # Pausar el sonido default
                if self.default_channel:
                    self.default_channel.stop()
                # Alternar entre pellet1 y pellet2
                if self.pellet_toggle:
                    self.pellet1_sound.play()
                else:
                    self.pellet2_sound.play()
                self.pellet_toggle = not self.pellet_toggle
                # Esperar a que termine el sonido del pellet antes de reanudar default
                while pygame.mixer.get_busy():
                    pygame.time.delay(10)
                self.default_channel = self.default_sound.play(loops=-1)

        

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
        # Reproducir levelintro.wav una vez y esperar a que termine
        self.levelintro_sound.play()
        while pygame.mixer.get_busy():
            pygame.time.delay(10)
        # Cuando termina, reproducir default.wav en bucle
        self.default_channel = self.default_sound.play(loops=-1)

        #bucle principal del juego
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)  # Limitar a 60 FPS