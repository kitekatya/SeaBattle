import pygame

from menu import Menu


class Game:

    def __init__(self, width=940, height=500):
        self.run = True
        self.in_game = False
        self.width = width
        self.height = height
        self.game = None

    def start(self):
        pygame.init()
        screen = pygame.display.set_mode((self.width, self.height),
                                         pygame.RESIZABLE)
        pygame.display.set_caption("Sea Battle")
        menu = Menu(screen)
        menu.main_loop()
        pygame.quit()
