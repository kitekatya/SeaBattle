from theme import Theme
import pygame


class ButtonRect:
    def __init__(self, x: int, y: int, rect: pygame.Rect, scale: int):
        self.width = rect.w
        self.height = rect.h
        self.rect = rect
        self.rect.topleft = (x, y)
        self.clicked = False

    def is_mouse_on(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def is_clicked(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        return action

    def change_top_left(self, pos: tuple[int, int]) -> None:
        self.rect.topleft = pos


class Button(ButtonRect):
    def __init__(self, x: int, y: int, image: str, theme: Theme,
                 scale: int, action: callable, action_on_mouse = None) -> None:
        if theme == Theme.dark:
            image = image[:image.rfind(".")] + '_dark' + image[image.rfind("."):]
        image = pygame.image.load(f'images/{image}').convert_alpha()
        super().__init__(x, y, image.get_rect(), scale)
        self.image = pygame.transform.scale(image, (int(self.width * scale),
                                                    int(self.height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x - image.get_width() // 2,
                             y - image.get_height() // 2)
        self.action = action
        self.action_on_mouse = action_on_mouse

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

    def change_top_left(self, pos: tuple[int, int]) -> None:
        self.rect.update(pos[0] - self.image.get_width() // 2,
                         pos[1] - self.image.get_height() // 2,
                         self.rect.width, self.rect.height)

    def __call__(self, *args, **kwargs):
        if not (len(args) == 1 and len(kwargs) == 0):
            raise TypeError

        self.draw(args[0].screen)

        if self.action_on_mouse:
            if self.is_mouse_on():
                self.action_on_mouse(*args, **kwargs)

        if self.is_clicked():
            self.action(*args, **kwargs)
