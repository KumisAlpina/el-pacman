import pygame
import constantes
import sys
from button import Button

pygame.init()

ancho = constantes.ANCHO_VENTANA
alto = constantes.ALTO_VENTANA

ventana = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("PAC-MAN")
fps = pygame.time.Clock()

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

def play():
    run = True
    while run:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        ventana.fill("black")

        PLAY_TEXT = get_font(45).render("Pantalla de juego", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(ancho//2, 260))
        ventana.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(pos=(ancho//2, 460),
                          text_input="VOLVER", font=get_font(75), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(ventana)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()

        pygame.display.update()
        fps.tick(60)

def options():
    run = True
    while run:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        ventana.fill("white")

        OPTIONS_TEXT = get_font(45).render("Pantalla de controles", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(ancho//2, 260))
        ventana.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(pos=(ancho//2, 460),
                            text_input="VOLVER", font=get_font(75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(ventana)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()
        fps.tick(60)

def main_menu():
    # Cargar la imagen del título
    titulo_imagen = pygame.image.load("assets/Titulo.jpg").convert_alpha()
    # Escalar la imagen si es necesario
    titulo_imagen = pygame.transform.scale(titulo_imagen, (600, 150))
    titulo_rect = titulo_imagen.get_rect(center=(ancho//2, 200))

    # Crear el texto PAC-MAN
    MENU_TEXT = get_font(75).render("PAC-MAN", True, constantes.AMARILLO)
    MENU_RECT = MENU_TEXT.get_rect(center=(ancho//2, 200))  # Misma posición que la imagen

    ventana.fill("black")
    run = True
    while run:
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        
        ventana.blit(titulo_imagen, titulo_rect)
        
        ventana.blit(MENU_TEXT, MENU_RECT)

        PLAY_BUTTON = Button(pos=(ancho//2, 410),
                            text_input="JUGAR", font=get_font(35), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(pos=(ancho//2, 480),
                            text_input="CONTROLES", font=get_font(35), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(pos=(ancho//2, 550),
                            text_input="SALIR", font=get_font(35), base_color="#d7fcd4", hovering_color="White")

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(ventana)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        fps.tick(60)

main_menu()