from enum import Enum


class MenuState(Enum):
    main = 0
    change_player_name = 1
    change_player_name_incorrect_name = 2
    score = 3
    prepare_to_game = 4
    game = 5
    end_game = 6
