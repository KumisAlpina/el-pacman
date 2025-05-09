import pygame
import constantes

pygame.init()

ancho = constantes.ANCHO_VENTANA
alto = constantes.ALTO_VENTANA

ventana = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("PAC-MAN")
fps = pygame.time.Clock()


run = True

fondo = pygame.image.load("PacMan_01.bmp").convert()

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: run = False

    # ---- LOGICA ----
    
    

    # ---- LOGICA ----

    ventana.blit(fondo, [0, 0])

    # ---- ZONA DE DIBUJO ----
    
    

    # ---- ZONA DE DIBUJO ----
    pygame.display.update()
    fps.tick(60)



pygame.quit()
