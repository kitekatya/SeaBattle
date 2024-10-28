from pygame import Surface as Surface
from pygame import font as fnt
from pygame import draw
from string import ascii_uppercase, ascii_lowercase
from ships import Ships
from ship import Ship


class Grid:
    def __init__(self, title: str, size_x: int, size_y: int,
                 left_margin: float | None = None,
                 upper_margin: float | None = None,
                 block_size: int | None = None):
        self.title = title
        self.size_x = size_x
        self.size_y = size_y
        self.left_margin = left_margin
        self.upper_margin = upper_margin
        self.block_size = block_size
        self.max_len_ship = 4 if max(self.size_x, self.size_y) > 4 \
            else min(self.size_x, self.size_y)
        self.count_of_ships = int((size_x * size_y) ** 0.5)
        self.number_of_ships = self.create_ships_dict(self.count_of_ships)
        self.ships = Ships(self.size_x, self.size_y, self.number_of_ships)
        self.hit_blocks = set()  # клетки, в которые стреляли
        self.dotted_blocks = set()  # клетки, в которые уже можно не стрелять
        self.available_cells = set((x, y) for x in range(1, size_x + 1)
                                   for y in range(1, size_y + 1))

    def create_ships_dict(self, count_ships: int):
        number_of_ships = {i: self.max_len_ship + 1 - i
                           for i in range(self.max_len_ship, 0, -1)}

        while count_ships > 10:
            number_of_ships[self.max_len_ship] += 1
            count_ships -= 1

        if count_ships < 10:
            current_count = sum(number_of_ships.values())
            while current_count != count_ships:
                number_of_ships[self.max_len_ship] -= 1
                if number_of_ships[self.max_len_ship] == 0:
                    number_of_ships.pop(self.max_len_ship)
                    self.max_len_ship -= 1
                current_count -= 1

        return number_of_ships


    def update_params(self, left_margin: float, upper_margin: float,
                      block_size: int) -> None:
        self.left_margin = left_margin
        self.upper_margin = upper_margin
        self.block_size = block_size

    def is_coord_on_grid(self, coord: tuple[int, int]) -> bool:
        return (self.left_margin <= coord[0] <= self.get_right_margin() and
                self.upper_margin <= coord[1] <= self.get_down_margin())

    def get_right_margin(self) -> float | None:
        if all(i is not None for i in [self.left_margin, self.block_size]):
            return self.left_margin + self.block_size * self.size_x
        return None

    def get_down_margin(self) -> float | None:
        if all(i is not None for i in [self.upper_margin, self.block_size]):
            return self.upper_margin + self.block_size * self.size_y
        return None

    def from_pixels_to_coords(self, coord: tuple[int, int]):
        return ((coord[0] - self.left_margin) // self.block_size + 1,
                (coord[1] - self.upper_margin) // self.block_size + 1)

    def from_coords_to_pixels(self, coord: tuple[int, int]):
        return (self.left_margin + self.block_size * (coord[0] - 1),
                self.upper_margin + self.block_size * (coord[1] - 1))

    def shuffle_ships(self, colour_ship) -> None:
        self.ships.auto_ship(colour_ship)

    def draw_turn(self, screen: Surface, text: str, colour='black') -> None:
        font_size = int(self.block_size / 1.5)
        font = fnt.SysFont('arial', font_size)
        turn = font.render(text, True, colour)

        screen.blit(turn, ((screen.get_width() - turn.get_width()) // 2,
                             self.upper_margin - turn.get_height() // 2))

    def draw_ship(self, screen: Surface, ship: list[tuple[int, int]],
                  colour) -> None:
        ship_width = self.block_size * (ship[-1][0] - ship[0][0] + 1)
        ship_height = self.block_size * (ship[-1][1] - ship[0][1] + 1)

        x = self.block_size * (ship[0][0] - 1) + self.left_margin
        y = self.block_size * (ship[0][1] - 1) + self.upper_margin

        draw.rect(screen, colour, ((x, y), (ship_width, ship_height)),
                  width=self.block_size // 10)

    def draw_ships(self, screen, ships_coordinates_list: list[Ship]):
        for elem in ships_coordinates_list:
            self.draw_ship(screen, elem.cells, elem.colour)

    def draw_destroyed_ships(self, screen):
        for ship in self.ships.ships:
            if not ship.is_alive:
                self.draw_ship(screen, ship.cells, ship.colour)

    def draw_hits(self, screen, colour):
        for hit in self.hit_blocks:
            self.draw_hit(screen, colour, hit)

    def draw_dots(self, screen, colour):
        for dot in self.dotted_blocks:
            self.draw_dot(screen, colour, dot)

    def draw_dot(self, screen, colour, cell):
        cell = (cell[0] - 1, cell[1] - 1)
        draw.circle(screen, colour,
                    (cell[0] * self.block_size + self.left_margin +
                     self.block_size // 2, cell[1] * self.block_size +
                     self.upper_margin + self.block_size // 2),
                    3, 2)

    def draw_hit(self, screen, colour, cell):
        cell = (cell[0] - 1, cell[1] - 1)
        draw.line(screen, colour, (cell[0] * self.block_size +
                                   self.left_margin,
                                   cell[1] * self.block_size +
                                   self.upper_margin),
                  (cell[0] * self.block_size + self.left_margin +
                  self.block_size,
                   cell[1] * self.block_size + self.upper_margin +
                  self.block_size), 1)
        draw.line(screen, colour, (cell[0] * self.block_size +
                                   self.left_margin,
                                   cell[1] * self.block_size +
                                   self.upper_margin + self.block_size),
                  (cell[0] * self.block_size + self.left_margin +
                   self.block_size,
                   cell[1] * self.block_size + self.upper_margin))

    def draw(self, screen: Surface, colour: str | tuple[int, int, int],
             title: str, current_theme,
             is_ships_visible: bool = False) -> None:
        self.draw_grid(screen, colour)
        self.add_nums_letters_to_grid(screen, colour)
        self.sign_grid(title, screen, colour)
        self.draw_hits(screen, 'red')
        self.draw_dots(screen, current_theme.value['dot_colour'])

        if is_ships_visible:
            self.draw_ships(screen, self.ships.ships)
        else:
            self.draw_destroyed_ships(screen)

    def draw_grid(self, screen: Surface, colour: str | tuple):
        for y in range(self.size_y + 1):
            draw.line(screen, colour,
                      (self.left_margin,
                          self.upper_margin + y * self.block_size),
                      (self.left_margin +
                          self.size_x * self.block_size,
                          self.upper_margin + y * self.block_size), 1)

        for x in range(self.size_x + 1):
            draw.line(screen, colour,
                      (self.left_margin + x * self.block_size,
                          self.upper_margin),
                      (self.left_margin + x * self.block_size,
                          self.upper_margin + self.size_y * self.block_size), 1)

    def add_nums_letters_to_grid(self, screen: Surface,
                                 colour: str | tuple[int, int, int]) -> None:
        font_size = int(self.block_size / 1.5)
        font = fnt.SysFont('arial', font_size)
        letters = ascii_uppercase + ascii_lowercase

        for i in range(self.size_x):
            letters_hor = font.render(letters[i], True, colour)
            screen.blit(letters_hor,
                        (self.left_margin + i * self.block_size +
                         (self.block_size // 2 - letters_hor.get_width() // 2),
                         self.upper_margin + self.size_y * self.block_size))

        for i in range(self.size_y):
            num_ver = font.render(str(i + 1), True, colour)
            screen.blit(num_ver, (
                self.left_margin -
                (self.block_size // 2 + num_ver.get_width() // 2),
                self.upper_margin + i * self.block_size + (
                        self.block_size // 2 - num_ver.get_height() // 2)))

    def sign_grid(self, title: str, screen: Surface, colour: str | tuple) -> \
            None:
        font_size = int(self.block_size / 1.5)
        font = fnt.SysFont('arial', font_size)
        player = font.render(title, True, colour)

        screen.blit(player, (self.left_margin + self.size_x // 2 *
                             self.block_size - player.get_width() // 2,
                             self.upper_margin - self.block_size // 2 -
                             player.get_height() // 2))
