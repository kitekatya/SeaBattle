import pytest
from ship import Ship
from ships import Ships
from grid import Grid
from player import Player
import pygame


def create_ship(cells: list[tuple[int, int]]) -> Ship:
    ship = Ship()
    ship.add_cells(cells)
    return ship


def create_ships() -> Ships:
    size_x = 5
    size_y = 5
    number_of_ships = {1: 1, 2: 2}
    ships = Ships(size_x, size_y, number_of_ships)
    return ships


def create_grid() -> Grid:
    return Grid('player', 10, 10)


class TestShips:
    def test_defaults(self):
        """Testing default ships on grid"""
        size_x = 5
        size_y = 5
        number_of_ships = {1: 1, 2: 2, 3: 1}
        ships = Ships(size_x, size_y, number_of_ships)
        assert len(ships.ships) == 4
        assert ships.ships[0] == create_ship([(1, 7)])
        assert ships.ships[1] == create_ship([(1, 9), (2, 9)])
        assert ships.ships[2] == create_ship([(4, 9), (5, 9)])
        assert ships.ships[3] == create_ship([(1, 11), (2, 11), (3, 11)])
        assert ships.ships_set == set()

    def test_auto_ship(self):
        """Testing auto ships on grid"""
        ships = create_ships()
        ships.auto_ship()
        assert len(ships.ships_set) == 1 + 2 * 2
        assert len(ships.ships[0].cells) == 1
        assert len(ships.ships[1].cells) == 2
        assert len(ships.ships[2].cells) == 2
        for i in range(2):
            for j in range(i + 1):
                assert 1 <= ships.ships[i].cells[j][0] <= ships.size_x
                assert 1 <= ships.ships[i].cells[j][1] <= ships.size_y

    def test_get_neighbours_cells(self):
        """Testing get_neighbours_cells on grid"""
        ships = create_ships()
        neighbours = ships.get_neighbours((2, 2))
        assert neighbours == {(1, 1), (2, 1), (3, 1),
                              (1, 2), (2, 2), (3, 2),
                              (1, 3), (2, 3), (3, 3)}

    def test_get_neighbours_cells_on_edge(self):
        """Testing get_neighbours_cells on edge grid"""
        ships = create_ships()
        neighbours = ships.get_neighbours((1, 1))
        assert neighbours == {(1, 1), (2, 1),
                              (1, 2), (2, 2)}

    def test_get_neighbours_cells_without_diagonal(self):
        """Testing get_neighbours_cells on edge grid without diagonal"""
        ships = create_ships()
        neighbours = ships.get_neighbours((1, 1), diagonalized=False)
        assert neighbours == {(1, 1), (2, 1),
                              (1, 2)}

    def test_get_neighbours_cells_without_cell(self):
        """Testing get_neighbours_cells on edge grid without this cell"""
        ships = create_ships()
        neighbours = ships.get_neighbours((1, 1), this_cell=False)
        assert neighbours == {(2, 1),
                              (1, 2), (2, 2)}

    def test_get_neighbours_cells_for_ship_not_on_grid(self):
        """Testing get_neighbours_cells_for_ship not on the grid"""
        ships = create_ships()
        neighbours = ships.get_neighbours_cells_for_ship(ships.ships[0])
        assert neighbours == set()


class TestGrid:
    @pytest.fixture
    def init_grid(self):
        grid = Grid('', size_x=10, size_y=10, block_size=20,
                    left_margin=50, upper_margin=50)
        return grid

    @pytest.fixture
    def init_screen(self):
        screen = pygame.Surface((800, 600))
        screen.fill('white')
        return screen

    def test_shuffle_on_grid(self):
        """Testing shuffle_on_grid"""
        grid = create_grid()
        grid.shuffle_ships('')
        assert len(grid.ships.ships) == sum(i for i in grid.number_of_ships)
        assert len(grid.ships.ships_set) == sum(
            i * grid.number_of_ships[i] for i in
            grid.number_of_ships)

    def test_colour_shuffle_on_grid(self):
        """Testing shuffle with colour on grid"""
        grid = create_grid()
        grid.shuffle_ships('black')
        for ship in grid.ships.ships:
            assert ship.colour == 'black'

    def test_create_ships_dict_default(self, init_grid):
        """Testing create_ships_dict with correct numbers of ships default"""
        grid = init_grid
        ships = grid.create_ships_dict(10)
        assert ships == {1: 4, 2: 3, 3: 2, 4: 1}

    def test_create_ships_dict_less_than_10(self, init_grid):
        """Testing create_ships_dict with correct numbers of ships < 10"""
        grid = init_grid
        ships = grid.create_ships_dict(7)
        assert ships == {1: 4, 2: 3}

    def test_create_ships_dict_more_than_10(self, init_grid):
        """Testing create_ships_dict with correct numbers of ships > 10"""
        grid = init_grid
        ships = grid.create_ships_dict(15)
        assert ships == {1: 4, 2: 3, 3: 2, 4: 6}

    def test_draw_grid(self, init_grid, init_screen):
        """Testing draw_grid"""
        grid = init_grid
        screen = init_screen
        grid.draw_grid(screen, 'black')

        assert screen.get_at((50, 50)) == (0, 0, 0, 255)
        assert screen.get_at((51, 51)) == (255, 255, 255, 255)
        assert screen.get_at((50 + grid.size_x * grid.block_size, 50)) == (
        0, 0, 0, 255)
        assert screen.get_at((50, 50 + grid.size_y * grid.block_size)) == (
        0, 0, 0, 255)

    def test_is_coord_not_on_grid(self, init_grid):
        """Testing is_coord_not_on_grid when not on grid"""
        assert init_grid.is_coord_on_grid((800, 800)) == False

    def test_is_coord_on_grid(self, init_grid):
        """Testing is_coord_not_on_grid when on grid"""
        assert init_grid.is_coord_on_grid((50, 50))

    def test_from_pixels_to_coordinates(self, init_grid):
        """Testing from_pixels_to_coordinates at start position"""
        assert init_grid.from_pixels_to_coords((50, 50)) == (1, 1)

    def test_from_coordinates_to_pixels(self, init_grid):
        """Testing from_pixels_to_coordinates when pixels not on grid"""
        assert init_grid.from_pixels_to_coords((49, 49)) == (0, 0)

    def test_from_coordinates_to_pixel(self, init_grid):
        """Testing from_pixels_to_coordinates at start position"""
        assert init_grid.from_coords_to_pixels((1, 1)) == (50, 50)

    def test_draw_turn(self, init_grid, init_screen):
        init_grid.draw_ship(init_screen, [(1, 1)], 'black')
        assert init_screen.get_at((50, 50)) == (0, 0, 0, 255)
        assert init_screen.get_at((55, 55)) == (255, 255, 255, 255)


class TestPlayer:
    def test_player_can_win(self):
        """Testing player can win"""
        player = Player('player', 10, 10)
        assert not player.is_winner()
        player.destroyed_ships = 10
        assert player.is_winner()

    def test_human_player_cant_auto_shoot(self):
        """Testing human can automatically shoot"""
        player = Player('player', 10, 10)
        opposite_grid = create_grid()
        with pytest.raises(Exception):
            player.auto_shot(opposite_grid)

    def test_human_can_manual_shoot_not_ship_cell(self):
        """Testing human can shooting on the grid on not ship cell"""
        player = Player('player', 10, 10)
        opposite_grid = create_grid()
        player.manual_shot((1, 1), opposite_grid)
        assert opposite_grid.dotted_blocks == {(1, 1)}
        assert opposite_grid.hit_blocks == set()

    def test_human_can_manual_shoot_ship_cell(self):
        """Testing human can shooting on the grid on ship cell"""
        player = Player('player', 10, 10)
        opposite_grid = create_grid()
        opposite_grid.ships.ships_set.add((1, 1))
        player.manual_shot((1, 1), opposite_grid)
        assert opposite_grid.hit_blocks == {(1, 1)}
        assert opposite_grid.dotted_blocks == set()

    def test_computer_can_auto_shoot_on_not_ship_cell(self):
        """Testing computer can automatically shoot on not ship cell"""
        player = Player('player', 10, 10, is_computer=True)
        opposite_grid = create_grid()
        player.auto_shot(opposite_grid)
        assert len(opposite_grid.dotted_blocks) == 1
        assert opposite_grid.hit_blocks == set()

    def test_computer_can_auto_shoot_on_ship_cell(self):
        """Testing computer can automatically shoot on ship cell"""
        player = Player('player', 10, 10, is_computer=True)
        opposite_grid = create_grid()
        opposite_grid.ships.ships_set |= {(i, j) for i in range(1, 11)
                                          for j in range(1, 11)}
        player.auto_shot(opposite_grid)
        assert len(opposite_grid.hit_blocks) == 1
        assert opposite_grid.dotted_blocks == set()

    def test_dot_space_destroyed_ship(self):
        """Testing that after ship killing neighbours cells are dotted"""
        player = Player('', 10, 10)
        opposite_grid = create_grid()
        ship = opposite_grid.ships.ships[-1]
        ship.cells = [(1, 1)]
        opposite_grid.ships.manual_place_ship(ship)
        player.manual_shot((1, 1), opposite_grid)
        assert player.destroyed_ships == 1
        assert {(1, 1), (1, 2), (2, 1),
                (2, 2)} not in opposite_grid.available_cells

    def test_cant_manual_place_new_ship(self):
        """Testing that ship count cant increase"""
        opposite_grid = create_grid()
        ship = create_ship([(1, 1)])
        with pytest.raises(Exception):
            opposite_grid.ships.manual_place_ship(ship)

    def test_cant_manual_place_incorrect_ship_near(self):
        """Testing that ship can't be placed incorrectly (near)"""
        opposite_grid = create_grid()
        ship = opposite_grid.ships.ships[-1]
        ship.cells = [(1, 1)]
        opposite_grid.ships.manual_place_ship(ship)
        ship = opposite_grid.ships.ships[-2]
        ship.cells = [(1, 2)]
        with pytest.raises(Exception):
            opposite_grid.ships.manual_place_ship(ship)

    def test_cant_manual_place_incorrect_ship_on_same_cell(self):
        """Testing that ship can't be placed incorrectly (on same cell)"""
        opposite_grid = create_grid()
        ship = opposite_grid.ships.ships[-1]
        ship.cells = [(1, 1)]
        opposite_grid.ships.manual_place_ship(ship)
        ship = opposite_grid.ships.ships[-2]
        ship.cells = [(1, 1)]
        with pytest.raises(Exception):
            opposite_grid.ships.manual_place_ship(ship)
