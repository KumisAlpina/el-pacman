import pygame
import sys
from game import Game

def main():
    try:
        #iniciar pygame
        pygame.init()

        #crear el juego
        game = Game()
        game.run()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    finally:
        #cerrar pygame
        pygame.quit()
        sys.exit()
    
if __name__ == "__main__":
    main()  
