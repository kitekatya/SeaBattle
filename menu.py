import pygame
import button
from seaBattle import SeaBattle
from pygame import Surface
from pygame import font as fnt
from user_input import UserInput
from ship import Ship
from buttons import Buttons
from Score import get_scores
from MenuStates import MenuState
from player import Player
from theme import Theme

class Menu:
    def __init__(self, screen: Surface):
        self.screen: Surface = screen
        self.menu_state: MenuState = MenuState.main
        self.run: bool = True
        self.left_margin, self.upper_margin = 50, 50
        self.font_size: int = 50
        self.theme: Theme = Theme.light
        self.sea_battle: SeaBattle | None = None
        self.buttons: Buttons = Buttons(self.theme)

        self.player_name: str = self.change_name()
        self.player2_name: str | None = None

        self.size_x: int = 10
        self.size_y: int = 10

        self.selected_ship: Ship | None = None
        self.cell_selected_ship: int | None = None

    def is_ship_selected(self):
        return self.selected_ship is not None

    def main_loop(self):
        scores = None
        while self.run:
            for event in pygame.event.get():
                pygame.display.update()
                if event.type == pygame.QUIT:
                    self.run = False
                if self.menu_state == MenuState.main:
                    self.draw_main()
                elif self.menu_state == MenuState.score:
                    if scores is None:
                        scores = get_scores()
                    self.draw_scores(scores)
                elif self.menu_state == MenuState.game:
                    self.sea_battle.start()
                    if self.sea_battle.exit_pressed: self.run = False
                    self.menu_state = MenuState.end_game
                elif self.menu_state == MenuState.prepare_to_game:
                    self.prepare_to_game()
                    if (event.type == pygame.MOUSEBUTTONDOWN and not
                        self.is_ship_selected() and self.sea_battle):
                        self.select_ship(event)
                    elif (event.type == pygame.MOUSEBUTTONUP and
                      self.is_ship_selected() and self.sea_battle):
                        self.move_ship(event.pos)
                        self.prepare_to_game()
                elif self.menu_state == MenuState.end_game:
                    self.draw_end(self.sea_battle.winner)
                    scores = None
                pygame.display.flip()

    def draw_change_name(self, event, user_input, busy_name: str | None):
        background = self.theme.value['background_colour']
        main = self.theme.value['main_colour']
        self.screen.fill(background)
        x, y = self.screen.get_width() // 2, int(self.screen.get_height() // 2.5)
        self.draw_text('Введите имя:', (x, y), main, background)
        user_input.add(event)
        y += self.render_text(user_input.user_input, main).get_height() * 2
        self.draw_text(user_input.user_input, (x, y), main, background)
        y += self.render_text('Готово', main).get_height() * 2
        ok_rect = self.draw_text('Готово', (x, y), main, background)
        button_ok = button.ButtonRect(*ok_rect.topleft, ok_rect, 1)

        if self.menu_state == MenuState.change_player_name_incorrect_name:
            if (event.type != pygame.KEYDOWN and user_input.user_input
                    == ''):
                self.draw_text('Имя не может быть пустым',
                               (x, y + 1.5 * ok_rect.height), main, background)
            elif (event.type != pygame.KEYDOWN and user_input.user_input ==
                    busy_name):
                self.draw_text('Имя уже занято',
                               (x, y + 1.5 * ok_rect.height), main, background)
            else:
                self.menu_state = MenuState.change_player_name
        if button_ok.is_clicked() or (event.type == pygame.KEYDOWN
                and event.key == pygame.K_RETURN):
            if (user_input.user_input != '' and len(user_input.user_input) <=
                    user_input.max_symbols + 1 and
                    user_input.user_input != busy_name):
                self.menu_state = MenuState.main
            else:
                self.menu_state = MenuState.change_player_name_incorrect_name
        self.draw_change_theme()
        pygame.display.update()

    def change_name(self, busy_name: str | None = None) -> str:
        user_input = UserInput()
        prev_state = self.menu_state
        self.menu_state = MenuState.change_player_name
        while (self.run and (self.menu_state == MenuState.change_player_name or
               self.menu_state == MenuState.change_player_name_incorrect_name)):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                self.draw_change_name(event, user_input, busy_name)

        self.menu_state = prev_state
        return user_input.user_input

    def render_text(self, text: str, colour='white') -> Surface:
        font = fnt.SysFont('Aptos ExtraBold', self.font_size)
        return font.render(text, True, colour)

    def draw_text(self, text: str, top_left: tuple[int, int],
                  text_colour='white', bckgrnd_colour='black'):
        text = self.render_text(text, text_colour)
        top_left = max(top_left[0] - text.get_width() // 2, 0), top_left[1]
        rect = pygame.draw.rect(self.screen, text_colour,
                         (top_left, (text.get_width() + 20,
                                    text.get_height() + 15)))
        pygame.draw.rect(self.screen, bckgrnd_colour,
                                     ((top_left[0] + 5, top_left[1] + 5),
                                      (text.get_width() + 10,
                                       text.get_height() + 5)))
        self.screen.blit(text, (top_left[0] + 10,
                                top_left[1] + 10))
        return rect

    def draw_main(self):
        background = self.theme.value['background_colour']
        main = self.theme.value['main_colour']

        self.screen.fill(background)
        button_name = button.ButtonRect(5, 5, self.draw_text(
            self.player_name, (0, 0), main, background), 1)

        x = self.screen.get_width() // 2
        y = int(self.screen.get_height() // 2.5)
        self.buttons.resume_button.change_top_left((x, y))
        y += int(self.buttons.resume_button.image.get_height())

        score_rect = self.draw_text('SCORE', (x, y), main, background)
        button_score = button.ButtonRect(*score_rect.topleft, score_rect, 1)

        self.buttons.resume_button(self)
        self.draw_change_theme()

        if button_name.is_clicked():
            self.player_name = self.change_name()
        if button_score.is_clicked():
            self.menu_state = MenuState.score

    def move_ship(self, pos: tuple[int, int]) -> None | int:
        selected_colour = self.theme.value['selected_ship_colour']
        player = self.sea_battle.get_current_player()
        ship = self.selected_ship
        number_cell = self.cell_selected_ship

        x, y = player.grid.from_pixels_to_coords(pos)
        if not player.grid.is_coord_on_grid(pos):
            return
        if (x, y) in ship.cells:
            self.cell_selected_ship = ship.cells.index((x, y))
            return

        ship.cells = [(x + (-number_cell + i) * (not ship.is_vert),
                       y + (-number_cell + i) * ship.is_vert)
                      for i in (range(ship.length))]

        if not player.grid.ships.is_ship_valid(ship.cells):
            ship.colour = 'red'
        else:
            ship.colour = selected_colour

        self.cell_selected_ship = number_cell

    def select_ship(self, event):
        selected_colour = self.theme.value['selected_ship_colour']
        player = self.sea_battle.get_current_player()
        x, y = player.grid.from_pixels_to_coords(event.pos)
        for ship in player.grid.ships.ships:
            if (x, y) in ship.cells:
                ship.colour = selected_colour
                if (player.grid.size_x >= ship.cells[0][0] >= 0 and
                        player.grid.size_y >= ship.cells[0][1] >= 0):
                    player.grid.ships.available_blocks |= \
                        player.grid.ships.get_neighbours_cells_for_ship(ship)
                    for ship1 in player.grid.ships.ships:
                        if ship1 != ship:
                            player.grid.ships.available_blocks -= (
                                player.grid.ships
                                .get_neighbours_cells_for_ship(ship1))
                    player.grid.ships.ships_set -= set(ship.cells)
                self.selected_ship = ship
                self.cell_selected_ship = x % (ship.length + 1) - 1

    def draw_choose_players(self):
        background = self.theme.value['background_colour']
        main = self.theme.value['main_colour']

        self.screen.fill(background)
        self.buttons.alone_button.change_top_left((self.screen.get_width() // 3,
                                           self.screen.get_height() // 2))
        self.buttons.with_friend_button.change_top_left((int(self.screen.get_width() // 1.5),
                                           self.screen.get_height() // 2))
        self.buttons.back_button.change_top_left((self.screen.get_width() - self.buttons.back_button.rect.width // 2,
                                                  self.screen.get_height() - 2 * self.buttons.theme_button.rect.height - self.buttons.back_button.height))

        self.buttons.alone_button(self)
        self.buttons.with_friend_button(self)
        self.buttons.back_button(self)
        self.draw_change_theme()

        pygame.display.update()

    def prepare_to_game(self) -> None:
        if not self.sea_battle:
            self.draw_choose_players()
            return

        self.update_colour_on_ships()

        left_margin, upper_margin, block_size, size_y, size_x = (
            self.sea_battle.player1.grid.left_margin,
            self.sea_battle.player1.grid.upper_margin,
            self.sea_battle.player1.grid.block_size,
            self.sea_battle.player1.grid.size_y,
            self.sea_battle.player1.grid.size_x)

        background = self.theme.value['background_colour']

        self.screen.fill(background)
        self.sea_battle.update_params(*self.screen.get_size())
        up = upper_margin + (size_y + 2) * block_size
        left = left_margin + max(size_x + 2, 10) * block_size
        left = max(left, self.screen.get_width() // 2)
        self.buttons.auto_button.change_top_left((left, up))
        self.buttons.play_button.change_top_left(
            (left + 2 * self.buttons.auto_button.width, up))
        self.buttons.back_button.change_top_left((self.screen.get_width() -
                                                  left_margin // 2,
                                                  self.screen.get_height()
                                                  - 2 * self.buttons.theme_button.rect.height
                                                  - self.buttons.back_button.height))

        self.buttons.plus_x_button.change_top_left(
            (15, 15))
        self.buttons.minus_x_button.change_top_left(
            (self.buttons.plus_x_button.width * 2, 15))

        self.buttons.plus_y_button.change_top_left(
            (15, 80))
        self.buttons.minus_y_button.change_top_left(
            (15, 110))

        self.sea_battle.draw_grid(self.screen)

        self.buttons.auto_button(self)
        self.buttons.play_button(self)
        if self.sea_battle.player2.is_computer or self.sea_battle.is_plr1_turn:
            self.buttons.plus_x_button(self)
            self.buttons.minus_x_button(self)
            self.buttons.plus_y_button(self)
            self.buttons.minus_y_button(self)
        self.buttons.back_button(self)

        self.draw_change_theme()

        if self.is_ship_selected():
            self.draw_button_for_ship()

    def draw_button_for_ship(self):
        player = self.sea_battle.get_current_player()

        left_margin, upper_margin, block_size, size_y, size_x = (
            self.sea_battle.player1.grid.left_margin,
            self.sea_battle.player1.grid.upper_margin,
            self.sea_battle.player1.grid.block_size,
            self.sea_battle.player1.grid.size_y,
            self.sea_battle.player1.grid.size_x)

        up = upper_margin + (size_y // 2) * block_size
        left = player.grid.left_margin + (size_x + 1) * block_size
        self.buttons.rotate_button.change_top_left((left, up))
        up += 1.5 * self.buttons.rotate_button.rect.height
        self.buttons.done_button.change_top_left((left, up))

        self.buttons.rotate_button(self)
        self.buttons.done_button(self)

    def draw_scores(self, scores):
        background = self.theme.value['background_colour']
        main = self.theme.value['main_colour']

        self.screen.fill(background)
        x, y = 0, 0
        for i, score in enumerate(scores):
            name = score['player_name']
            score = score['score']
            rect = self.draw_text(f'{i+1}) {name}: {score}', (x, y), main, background)
            y += 1.5 * rect.height
        back = self.draw_text('Назад',
                              (self.screen.get_width() -
                               self.render_text('Назад').get_width(), 0),
                              'green', background)
        button_back = button.ButtonRect(*back.topleft, back, 1)
        if button_back.is_clicked():
            self.menu_state = MenuState.main
        self.draw_change_theme()

    def draw_end(self, winner: Player):
        background = self.theme.value['background_colour']
        main = self.theme.value['main_colour']

        self.screen.fill(background)
        self.draw_text(f'{winner.name} won with {winner.score}!',
                       (self.screen.get_width()//2,
                        self.screen.get_height()//2), main,
                       background)
        self.buttons.back_button(self)

    def draw_change_theme(self):
        self.buttons.theme_button.change_top_left((self.screen.get_width() -
                                                   self.buttons.theme_button.image.get_width(),
                                                   self.screen.get_height() -
                                                   self.buttons.theme_button.image.get_height()))
        self.buttons.theme_button(self)

    def update_colour_on_ships(self):
        selected_colour = self.theme.value['selected_ship_colour']
        for ship in self.sea_battle.player1.grid.ships.ships:
            if ship.colour == selected_colour or ship.colour == 'red': continue
            ship.colour = self.theme.value['ship_colour']
        for ship in self.sea_battle.player2.grid.ships.ships:
            if ship.colour == selected_colour or ship.colour == 'red': continue
            ship.colour = self.theme.value['ship_colour']

