import random
from ship import Ship


class Ships:
    def __init__(self, size_x: int, size_y: int,
                 number_of_ships: dict[int, int]):
        self.available_blocks = set((x, y)
                                    for x in range(1, size_x + 1)
                                    for y in range(1, size_y + 1))
        self.size_x = size_x
        self.size_y = size_y
        self.number_of_ships = number_of_ships
        self.ships_set = set()
        self.ships = self.default_ships()

    def default_ships(self):
        ships = []
        for length in self.number_of_ships:
            for num in range(self.number_of_ships[length]):
                ship = Ship()
                cells = [(_ + (length + 1) * num + 1, self.size_y + 2 * length)
                         for _ in range(length)]
                ship.add_cells(cells)
                ships.append(ship)
        return ships

    def auto_ship(self, colour_ship='black'):
        self.available_blocks = set((x, y)
                                    for x in range(1, self.size_x + 1)
                                    for y in range(1, self.size_y + 1))
        self.ships_set = set()
        self.ships = self.populate_grid(colour_ship)

    def is_all_ships_on_grid(self):
        return len(self.ships_set) == sum([length * self.number_of_ships[length]
                                           for length in self.number_of_ships])

    def manual_place_ship(self, ship: Ship):
        if not self.is_ship_valid(ship.cells) or ship not in self.ships:
            raise Exception("Can't place ship")
        self.ships_set.update(ship.cells)
        self.available_blocks -= self.get_neighbours_cells_for_ship(ship)

    @staticmethod
    def create_start_block(available_blocks: set[tuple[int, int]])\
            -> (int, int, int, int):
        is_vert = random.randint(0, 1)  # 0 гориз-ый, 1 вертик-ый
        dir_axis = random.choice((-1, 1))  # направление оси
        x, y = random.choice(tuple(available_blocks))
        return x, y, is_vert, dir_axis

    def create_ship(self, len_ship: int,
                    available_blocks: set[tuple[int, int]]) -> Ship:
        x, y, is_vert, dir_axis = self.create_start_block(available_blocks)
        ship_ = Ship(is_vert)
        for _ in range(len_ship):
            ship_.add_cell((x, y))
            if not is_vert:
                dir_axis, x = self.add_block_to_ship(
                    x, dir_axis, is_vert, ship_.cells)
            else:
                dir_axis, y = self.add_block_to_ship(
                    y, dir_axis, is_vert, ship_.cells)

        if self.is_ship_valid(ship_.cells):
            ship_.is_vert = is_vert
            return ship_
        return self.create_ship(len_ship, available_blocks)

    def add_block_to_ship(self, coord: int, dir_axis: int, is_vert: int,
                          ship_coordinates: list[tuple[int, int]]) \
            -> tuple[int, int]:
        if ((coord <= 1 and dir_axis == -1) or
                dir_axis == 1 and ((coord >= self.size_y and is_vert) or
                                   (coord >= self.size_x and not is_vert))):
            dir_axis *= -1
            return dir_axis, ship_coordinates[0][is_vert] + dir_axis
        else:
            return dir_axis, ship_coordinates[-1][is_vert] + dir_axis

    def is_ship_valid(self, new_ship: list[tuple[int, int]]) -> bool:
        return set(new_ship).issubset(self.available_blocks)

    def add_new_ship_to_set(self, new_ship: list[tuple[int, int]]) -> None:
        self.ships_set.update(new_ship)

    def get_neighbours(self, coord: tuple[int, int], diagonalized: bool = True,
                       this_cell: bool = True) -> set[tuple[int, int]]:
        neighbours = (set((coord[0] + k, coord[1] + m)
                          for k in range(-1, 2)
                          for m in range(-1, 2)
                          if (0 < (coord[0] + k) < (self.size_x + 1) and
                              0 < (coord[1] + m) < (self.size_y + 1))))
        if not this_cell:
            neighbours.discard(coord)
        if not diagonalized:
            neighbours.difference_update(set((coord[0] + k, coord[1] + m)
                                         for k in [-1, 1]
                                             for m in [-1, 1]))
        return neighbours

    def get_neighbours_cells_for_ship(self, ship: Ship) \
            -> set[tuple[int, int]]:
        neighbours = set()
        for cell in ship.cells:
            neighbours.update(self.get_neighbours(cell))
        return neighbours

    def update_available_blocks_for_creating_ships(self, new_ship: Ship)\
            -> None:
        for cell in new_ship.cells:
            (self.available_blocks
             .difference_update(self.get_neighbours(cell)))

    def populate_grid(self, colour_ship: str) -> list[Ship]:
        ships_coordinates_list = []

        for number_of_blocks in self.number_of_ships:
            for _ in range(self.number_of_ships[number_of_blocks]):
                new_ship = self.create_ship(
                    number_of_blocks, self.available_blocks)
                new_ship.colour = colour_ship
                ships_coordinates_list.append(new_ship)
                new_ship.cells.sort()
                self.add_new_ship_to_set(new_ship.cells)
                self.update_available_blocks_for_creating_ships(new_ship)
        return ships_coordinates_list
