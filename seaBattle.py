import pygame
from player import Player
from Score import insert_score
from theme import Theme


class SeaBattle:

    def __init__(self, width, height, player1: Player, player2: Player,
                 theme: Theme,
                 size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y
        self.theme = theme
        self.width = width
        self.height = height
        self.player1 = player1
        self.player2 = player2
        self.winner = None
        self.game_started = False
        self.exit_pressed = False
        self.is_plr1_turn = True

        self.update_params(width, height)

    def change_size_grid(self, size_x: int, size_y: int):
        self.size_x = size_x
        self.size_y = size_y
        self.player1.change_size_of_grid(size_x, size_y)
        self.player2.change_size_of_grid(size_x, size_y)
        self.update_params(self.width, self.height)

    def get_current_player(self):
        return self.player1 if self.is_plr1_turn else self.player2

    def update_params(self, width, height):
        self.width = width
        self.height = height

        left_margin = self.width // (2 * self.size_x)
        if left_margin < 50:
            left_margin = 50

        upper_margin = self.height // (2 * self.size_y)
        if upper_margin < 50:
            upper_margin = 50

        block_size = int(min(
            (self.width - 2 * left_margin) // (2.25 * self.size_x),
            (self.height - 2 * upper_margin) // (1.75 * self.size_y)))
        if block_size < 15:
            block_size = 15

        distance_between_grids = int((self.width - 2 * (
                left_margin + self.size_x * block_size)) / block_size)
        if distance_between_grids < 2:
            distance_between_grids = 2

        self.player1.grid.update_params(left_margin, upper_margin, block_size)
        self.player2.grid.update_params(left_margin +
                                        (self.size_x +
                                         distance_between_grids)
                                        * block_size, upper_margin, block_size)

    def is_robot_move(self):
        return (self.is_plr1_turn and self.player1.is_computer or
                not self.is_plr1_turn and self.player2.is_computer)

    def make_manual_move(self, pos_on_screen: tuple[int, int]):
        if self.is_plr1_turn and not self.player1.is_computer:
            if not self.player2.grid.is_coord_on_grid(pos_on_screen):
                return
            cell = self.player2.grid.from_pixels_to_coords(pos_on_screen)
            if cell not in self.player2.grid.available_cells:
                return
            ind = self.player1.manual_shot(cell, self.player2.grid)
            self.play_sound(ind != -1)
            self.is_plr1_turn = ind != -1
        elif not self.is_plr1_turn and not self.player2.is_computer:
            if not self.player1.grid.is_coord_on_grid(pos_on_screen):
                return
            cell = self.player1.grid.from_pixels_to_coords(pos_on_screen)
            if cell not in self.player1.grid.available_cells:
                return
            ind = self.player2.manual_shot(cell, self.player1.grid)
            self.play_sound(ind != -1)
            self.is_plr1_turn = ind == -1
        self.check_winners()

    def make_auto_move(self):
        if not self.is_plr1_turn and self.player2.is_computer:
            ind = self.player2.auto_shot(self.player1.grid)
            self.play_sound(ind != -1)
            self.is_plr1_turn = ind == -1
        elif self.is_plr1_turn and self.player1.is_computer:
            ind = self.player1.auto_shot(self.player2.grid)
            self.play_sound(ind != -1)
            self.is_plr1_turn = ind != -1
        self.check_winners()

    def check_winners(self):
        if self.player1.is_winner():
            self.winner = self.player1
            self.game_started = False
            insert_score(self.player1.name, self.player1.score)
            if not self.player2.is_computer:
                insert_score(self.player2.name, self.player2.score)
        elif self.player2.is_winner():
            self.winner = self.player2
            self.game_started = False
            insert_score(self.player1.name, self.player1.score)
            if not self.player2.is_computer:
                insert_score(self.player2.name, self.player2.score)

    def start(self):
        pygame.mixer.init(11025)
        self.game_started = True
        screen = pygame.display.set_mode((self.width, self.height),
                                         pygame.RESIZABLE)
        pygame.display.set_caption("Sea Battle")

        while self.game_started:
            self.draw_all(screen)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_started = False
                    self.exit_pressed = True
                elif event.type == pygame.WINDOWRESIZED:
                    self.update_params(event.x, event.y)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.make_manual_move(event.pos)

            self.draw_all(screen)
            pygame.display.update()

            if self.is_robot_move():
                self.make_auto_move()
        self.game_started = False

    @staticmethod
    def play_sound(is_hit: bool) -> None:
        sound_hit = pygame.mixer.Sound('./sounds/popal.mp3')
        sound_dot = pygame.mixer.Sound('./sounds/promah.mp3')
        if is_hit:
            sound_hit.play()
        else:
            sound_dot.play()

    def draw_grid(self, screen):
        background = self.theme.value['background_colour']
        main = self.theme.value['grid_colour']
        selected = self.theme.value['selected']

        screen.fill(background)
        name1 = f'{self.player1.name}: {self.player1.score}'
        name2 = f'{self.player2.name}: {self.player2.score}'
        if (self.player2.is_computer or not self.player2.is_computer and
                self.is_plr1_turn and not self.game_started):
            self.player1.grid.draw(screen, selected, name1, self.theme, True)
            self.player2.grid.draw(screen, main, name2, self.theme)
        elif (not self.player2.is_computer and not self.is_plr1_turn and not
              self.game_started):
            self.player1.grid.draw(screen, main, name1, self.theme)
            self.player2.grid.draw(screen, selected, name2, self.theme, True)
        elif not self.player2.is_computer:
            self.player1.grid.draw(screen, main, name1, self.theme)
            self.player2.grid.draw(screen, main, name2, self.theme)

    def draw_all(self, screen) -> None:
        self.draw_grid(screen)
        if self.is_plr1_turn:
            self.player1.grid.draw_turn(screen, f'Ход {self.player1.name}',
                                        self.theme.value['main_colour'])
        else:
            self.player2.grid.draw_turn(screen, f'Ход {self.player2.name}',
                                        self.theme.value['main_colour'])

