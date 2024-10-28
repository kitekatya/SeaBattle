from enum import Enum


class Theme(Enum):
    light = {
        'num': 0,
        'background_colour': 'white',
        'main_colour': 'black',
        'selected': 'blue',
        'ship_colour': 'black',
        'grid_colour': 'black',
        'dot_colour': 'black',
        'selected_ship_colour': 'green'
        }
    dark = {
        'num': 1,
        'background_colour': 'black',
        'main_colour': 'white',
        'selected': 'light blue',
        'ship_colour': 'white',
        'grid_colour': 'gray',
        'dot_colour': 'white',
        'selected_ship_colour': 'light green'
    }

