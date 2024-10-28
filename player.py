import random
from grid import Grid
from pygame.time import delay
from ship import Ship


class Player:
    def __init__(self, name: str, size_x: int, size_y: int,
                 is_computer: bool = False):
        self.name = name
        self.is_computer = is_computer
        self.grid = Grid(name, size_x, size_y)
        self.score = 0
        self.destroyed_ships = 0
        if is_computer:
            self.grid.ships.auto_ship()
            self.last_ship_hits = []
            self.around_last_ship_hits = set()

    def change_size_of_grid(self, size_x: int, size_y: int):
        self.grid = Grid(self.name, size_x, size_y)
        if self.is_computer:
            self.grid.ships.auto_ship()

    def get_index_of_hit_ship(self, cell: tuple, opposite_grid: Grid) -> int:
        if cell not in opposite_grid.ships.ships_set:
            opposite_grid.dotted_blocks.add(cell)
            if self.is_computer:
                self.around_last_ship_hits.discard(cell)
            return -1

        self.score += 10

        opposite_grid.ships.ships_set.remove(cell)
        opposite_grid.hit_blocks.add(cell)

        for ind, ship in enumerate(opposite_grid.ships.ships):
            if cell in ship.cells:
                ship.length -= 1
                if self.is_computer:
                    self.update_around_last_hit(cell, ind, opposite_grid)
                    if ship.length > 0:
                        self.last_ship_hits.append(cell)
                    else:
                        self.last_ship_hits.clear()
                        self.around_last_ship_hits.clear()
                if ship.length == 0:
                    self.score += 10
                    ship.is_alive = False
                    self.destroyed_ships += 1
                    self.dot_space_destroyed_ship(ship, opposite_grid)
                return ind

    def dot_space_destroyed_ship(self, ship: Ship, opposite_grid: Grid)\
            -> None:
        if ship.is_alive:
            return
        for cell in ship.cells:
            neighbors = opposite_grid.ships.get_neighbours(cell,
                                                           this_cell=False)
            opposite_grid.dotted_blocks.update(neighbors)
            opposite_grid.available_cells.difference_update(neighbors)
        opposite_grid.dotted_blocks.difference_update(ship.cells)

    def update_around_last_hit(self, cell: tuple, ind: int,
                               opposite_grid: Grid) -> None:
        if ind != -1 and cell in self.around_last_ship_hits:
            if cell[0] == self.last_ship_hits[0][0]:
                self.around_last_ship_hits.update(
                    opposite_grid.ships.get_neighbours(cell, False, False))
                self.around_last_ship_hits.difference_update(
                    set(i for i in self.around_last_ship_hits if cell[0] != i[0]))
            else:
                self.around_last_ship_hits.update(
                    opposite_grid.ships.get_neighbours(cell, False, False))
                self.around_last_ship_hits.difference_update(
                    set(i for i in self.around_last_ship_hits if cell[1] != i[1]))
        elif ind != -1 and cell not in self.around_last_ship_hits:
            self.around_last_ship_hits.update(self.grid.ships.get_neighbours(
                cell, False, False))
        else:
            self.around_last_ship_hits.discard(cell)
        self.around_last_ship_hits -= opposite_grid.hit_blocks
        self.around_last_ship_hits -= opposite_grid.dotted_blocks

    def manual_shot(self, cell: tuple, opposite_grid: Grid) -> int:
        opposite_grid.available_cells.discard(cell)
        return self.get_index_of_hit_ship(cell, opposite_grid)

    def auto_shot(self, opposite_grid: Grid) -> int:
        if not self.is_computer:
            raise Exception('Auto shot only for computer')

        delay(700)
        if self.around_last_ship_hits:
            fired_cell = random.choice(tuple(self.around_last_ship_hits))
        else:
            fired_cell = random.choice(tuple(opposite_grid.available_cells))

        opposite_grid.available_cells.discard(fired_cell)
        return self.get_index_of_hit_ship(fired_cell, opposite_grid)

    def is_winner(self):
        return self.destroyed_ships == self.grid.count_of_ships
