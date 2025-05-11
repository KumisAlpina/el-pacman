import pygame
from config import *
import random

class Wall:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    
    def draw(self, screen):
        #dibujar pared en pantalla
        pygame.draw.rect(screen, WALL_COLOR, self.rect)
    
class Coin:
    def __init__(self, x, y):
        #pocicion monedas
        self.x = x * TILE_SIZE + TILE_SIZE // 2
        self.y = y * TILE_SIZE + TILE_SIZE // 2

        #Cargar sprite sheet de la moneda
        self.sprite_sheet = load_image('BigCoin.png')

        #Cargar frames de animacion
        self.frames = []
        for i in range(COIN_FRAMES):
            frame = pygame.Surface((16, 16), pygame.SRCALPHA)
            frame.blit(self.sprite_sheet, (0, 0), (i * 16, 0, 16, 16))
            frame = pygame.transform.scale(frame, (COIN_SIZE, COIN_SIZE))
            self. frames.append(frame)
        #variables de animaciion
        self.current_frame = 0
        self.animation_timer = pygame.time.get_ticks()

        #rectangulo de colisiones
        self.rect = self.frames[0].get_rect(center=(self.x, self.y))

    def update(self):
        """Actualizar animacion de la moneda"""
        current_time = pygame.time.get_ticks()
        if current_time - self.animation_timer > COIN_ANIMATION_SPEED:
            self.current_frame = (self.current_frame + 1) % COIN_FRAMES
            self.animation_timer = current_time

    def draw(self, screen):
        """dibujar moneda en pantalla"""
        screen.blit(self.frames[self.current_frame], self.rect)


class Ghost:
    def __init__(self, x, y, ghost_type):
        #posicion inicial del fantasma
        self.x = x * TILE_SIZE + TILE_SIZE // 2
        self.y = y * TILE_SIZE + TILE_SIZE // 2

        # Tipo de fantasmas y sus caracteristicas
        self.ghost_type = ghost_type
        self.speed = GHOST_SPEEDS[ghost_type]
        self.direction_change_time = GHOST_DIRECTION_TIMES[ghost_type]

        #cargar sprite del fantasma
        self.sprite_sheet = load_image(GHOST_SPRITES[ghost_type])

        #cargar frames de animacion
        self.frames = []
        for i in range(GHOST_ANIMATION_FRAMES):
            frame = pygame.Surface((16, 16), pygame.SRCALPHA)
            frame.blit(self.sprite_sheet, (0, 0), (i * 16, 0, 16, 16))
            frame = pygame.transform.scale(frame, (GHOST_SIZE, GHOST_SIZE))
            self.frames.append(frame)
        #variables de animacon
        self.current_frame = 0
        self.animation_timer = pygame.time.get_ticks()

        #variables de movimiento
        self.direction = random.randint(0, 3)
        self.direction_timer = pygame.time.get_ticks()
        self.rect = self.frames[0].get_rect(center=(self.x, self.y))
    
    def get_next_direction(self):
        """Determinar la siguiente direccion del fantasma"""
        if self.ghost_type == 'red':
            # el fantasma rojo elije una direccion aleatoria
            return random.randint(0, 3)
        elif self.ghost_type == 'blue':
            # el fantasma azul alterna entre vertical y horizontal
            if self.direction in [RIGHT, LEFT]:
                return random.choice([UP, DOWN])
            else:
                return random.choice([RIGHT, LEFT])
        elif self.ghost_type == 'orange':
            # el fantasma naranja se mueve en sentido horario
            return (self.direction + 1) % 4
        else:
            #el fantasma verde se mueve en sentido antihorario
            return (self.direction - 1) % 4
    
    def change_direcction(self, walls):
        """Cambiar la direccion del fantasma segun su tipo"""
        if self.ghost_type == 'red':
            # el rojo prueba todas las direcciones hasta obtener una valida
            directions = list(range(4))
            random.shuffle(directions)
            for new_dir in directions:
                if self.can_move_in_direction(new_dir, walls):
                    self.direction = new_dir
                    break
        
        else:
            # los demas sigeun su patron especifico
            new_dir = self.get_next_direction()
            if self.can_move_in_direction(new_dir, walls):
                self.direction = new_dir
            else:
                # si no pueden moverse en una direccion se mueven en una aleatoria
                self.direction = random.randint(0, 3)
        self.direction_timer = pygame.time.get_ticks()

    def can_move_in_direction(self, direction, walls):
        """comprobar si el fantasma puede moverse"""
        dx = dy = 0 
        if direction == RIGHT:
            dx = self.speed
        elif direction == LEFT:
            dx = -self.speed
        elif direction == UP:
            dy = -self.speed
        elif direction == DOWN:
            dy = self.speed

        test_rect = self.rect.copy()
        test_rect.x += dx
        test_rect.y += dy

        for wall in walls:
            if test_rect.colliderect(wall.rect):
                return False
            return True

    def move(self, walls):
        """mover fantasmas y manejar coliciones"""
        current_time = pygame.time.get_ticks()
        if current_time - self.direction_timer > self.direction_change_time:
            self.change_direcction(walls)

        # calcular movimiento de la direccion
        dx = dy = 0
        # calcular mov segun la direccion
        dx = dy = 0
        if self.direction == RIGHT:
            dx = self.speed
        elif self.direction == LEFT:
            dx = -self.speed
        elif self.direction == UP:
            dy = -self.speed
        elif self.speed == DOWN:
            dy = self.speed
        
        # comprobar colicion en la nueva posicion
        new_rect = self.rect.copy()
        new_rect.x += dx
        new_rect.y += dy

        # si hay colision cambiar de direccion
        can_move = True
        for wall in walls:
            if new_rect.colliderect(wall.rect):
                can_move = False
                self.change_direcction(walls)
                break
        # si no hay colicion actualizar posicion
        if can_move:
            self.x += dx
            self.y += dy
            self.rect.center = (self.x, self.y)
            
        

    def update(self, walls):
        """Actualizar el estado del fantasma"""
        # Actualizar animacion
        current_time = pygame.time.get_ticks()
        if current_time - self.animation_timer > GHOST_ANIMATION_SPEED:
            self.current_frame = (self.current_frame + 1) % GHOST_ANIMATION_FRAMES
            self.animation_timer = current_time

        # Actualizar el movimiento
        self.move(walls)

    def draw(self, screen):
        """Dibujar el fantasma en la pantalla"""
        screen.blit(self.frames[self.current_frame], self.rect)


class Player:
    def __init__(self, x, y):
        #posición inicial al centro de la pantalla
        self.x = x * TILE_SIZE + TILE_SIZE // 2
        self.y = y * TILE_SIZE + TILE_SIZE // 2

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
            

    def move(self, walls):
        """Mover al jugador según la entrada del usuario"""
        # Intentar movimiento en x
        if self.dx != 0:
            # Crear un rectángulo temporal para la nueva posición en x
            future_rect = self.rect.copy()
            future_rect.x += self.dx
            # Comprobar colisión en x
            if not any(future_rect.colliderect(wall.rect) for wall in walls):
                self.x += self.dx

        # Intentar movimiento en y
        if self.dy != 0:
            # Crear un rectángulo temporal para la nueva posición en y
            future_rect = self.rect.copy()
            future_rect.y += self.dy
            # Comprobar colisión en y
            if not any(future_rect.colliderect(wall.rect) for wall in walls):
                self.y += self.dy

        # Actualizar el rectángulo a la nueva posición
        self.rect.center = (self.x, self.y)

         # Mantener al jugador dentro de la pantalla
        if self.x > SCREEN_WIDTH - PLAYER_SIZE:
            self.x = 0
        elif self.x < 0:
            self.x = SCREEN_WIDTH - PLAYER_SIZE

        if self.y > SCREEN_HEIGHT - PLAYER_SIZE:
            self.y = 0
        elif self.y < 0:
            self.y = SCREEN_HEIGHT - PLAYER_SIZE

    def handle_input(self):
        #manejar entrada del usuario y actualizar la velocidad
        keys = pygame.key.get_pressed()

        #reiniciar la velocidad
        self.dx = 0
        self.dy = 0

        if keys[pygame.K_RIGHT]:
            self.dx = PLAYER_SPEED
            self.direction = RIGHT
        elif keys[pygame.K_LEFT]:
            self.dx = -PLAYER_SPEED
            self.direction = LEFT
        elif keys[pygame.K_UP]:
            self.dy = -PLAYER_SPEED
            self.direction = UP
        elif keys[pygame.K_DOWN]:
            self.dy = PLAYER_SPEED
            self.direction = DOWN

        #actualizar estado del movimiento
        self.is_moving = self.dx != 0 or self.dy != 0

    def check_collision(self, walls, dx=0, dy=0):
        """COMPROBAR SI HAY UNA COLISION"""
        #Crear un rectangulo temporal en una posicion futura
        future_react = self.rect.copy()
        future_react.x += dx
        future_react.y += dy

        #comprobar si hay colisiones con la pared
        for wall in walls:
            if future_react.colliderect(wall.rect):
                return True
        return False

    def update(self, walls):
        self.handle_input()
        self.update_animation()

        #actualizar la imagen
        self.update_image()
        self.move(walls)

        

        
    
    def draw(self, screen):
        #dibujar el jugador
        screen.blit(self.image, self.rect)