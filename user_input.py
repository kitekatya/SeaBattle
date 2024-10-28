import pygame


class UserInput:
    def __init__(self):
        self.user_input = ''
        self.max_symbols = 19

    def add(self, event: pygame.event.Event):
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_BACKSPACE:
            self.user_input = self.user_input[:-1]
        elif event.key == pygame.K_RETURN:
            return
        else:
            if len(self.user_input) > self.max_symbols:
                return
            self.user_input += event.unicode

    def clear(self):
        self.user_input = ''
