class Ship:
    def __init__(self, is_vert=0) -> None:
        self.length = 0
        self.is_alive = True
        self.cells = []
        self.colour = 'black'
        self.is_vert = is_vert

    def add_cell(self, cell: tuple[int, int]) -> None:
        self.length += 1
        self.cells.append(cell)

    def add_cells(self, cells: list[tuple[int, int]]) -> None:
        for cell in cells:
            self.add_cell(cell)

    def __eq__(self, other):
        return (self.length == other.length and self.is_alive ==
                other.is_alive and self.cells == other.cells and
                self.colour == other.colour and self.is_vert == other.is_vert)
