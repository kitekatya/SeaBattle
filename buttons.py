from MenuStates import MenuState
from button import Button
from player import Player
from seaBattle import SeaBattle
from theme import Theme


low = 6
upper = 20


def action_resume(menu):
    menu.menu_state = MenuState.prepare_to_game


def action_quit(menu):
    menu.run = False


def action_alone(menu):
    player1 = Player(menu.player_name, menu.size_x, menu.size_y)
    player2 = Player('computer', menu.size_x, menu.size_y, True)
    menu.sea_battle = SeaBattle(*menu.screen.get_size(), player1, player2,
                                menu.theme, menu.size_x, menu.size_y)


def action_with_friend(menu):
    menu.player2_name = menu.change_name(menu.player_name)
    player1 = Player(menu.player_name, menu.size_x, menu.size_y)
    player2 = Player(menu.player2_name, menu.size_x, menu.size_y)
    menu.sea_battle = SeaBattle(*menu.screen.get_size(), player1, player2,
                                menu.theme, menu.size_x, menu.size_y)


def action_play(menu):
    if (not menu.sea_battle.get_current_player()
            .grid.ships.is_all_ships_on_grid()):
        return
    if (menu.sea_battle.player2.is_computer or
            not menu.sea_battle.is_plr1_turn):
        menu.menu_state = MenuState.game
        menu.sea_battle.is_plr1_turn = True
    elif (not menu.sea_battle.player2.is_computer and
          menu.sea_battle.is_plr1_turn):
        menu.sea_battle.is_plr1_turn = False


def action_back(menu):
    menu.menu_state = MenuState.main
    menu.selected_ship = menu.cell_selected_ship = None
    menu.sea_battle = None


def action_auto(menu):
    menu.selected_ship = None
    menu.sea_battle.get_current_player().grid.shuffle_ships(
        menu.theme.value['ship_colour'])


def action_rotate(menu):
    selected_colour = menu.theme.value['selected_ship_colour']
    for ind, cell in enumerate(menu.selected_ship.cells):
        if ind == menu.cell_selected_ship: continue
        x, y = menu.selected_ship.cells[ind]
        if menu.selected_ship.is_vert:
            y_fix = menu.selected_ship.cells[menu.cell_selected_ship][
                1]
            menu.selected_ship.cells[ind] = x + (y - y_fix), y_fix
        else:
            x_fix = menu.selected_ship.cells[menu.cell_selected_ship][
                0]
            menu.selected_ship.cells[ind] = x_fix, y + (x - x_fix)

    if not (menu.sea_battle.get_current_player()
            .grid.ships.is_ship_valid(menu.selected_ship.cells)):
        menu.selected_ship.colour = 'red'
    else:
        menu.selected_ship.colour = selected_colour

    menu.selected_ship.is_vert = 1 - menu.selected_ship.is_vert


def action_plus_x(menu):
    if menu.size_x == upper: return
    menu.size_x += 1
    menu.selected_ship = None
    menu.sea_battle.change_size_grid(menu.size_x, menu.size_y)


def action_minus_x(menu):
    if menu.size_x == low: return
    menu.size_x -= 1
    menu.selected_ship = None
    menu.sea_battle.change_size_grid(menu.size_x, menu.size_y)


def action_plus_y(menu):
    if menu.size_y == upper: return
    menu.size_y += 1
    menu.selected_ship = None
    menu.sea_battle.change_size_grid(menu.size_x, menu.size_y)


def action_minus_y(menu):
    if menu.size_y == low: return
    menu.size_y -= 1
    menu.selected_ship = None
    menu.sea_battle.change_size_grid(menu.size_x, menu.size_y)


def action_done(menu):
    selected_colour = menu.theme.value['selected_ship_colour']
    player = menu.sea_battle.get_current_player()
    if menu.selected_ship.colour == selected_colour:
        menu.selected_ship.colour = menu.theme.value['main_colour']
        player.grid.ships.manual_place_ship(menu.selected_ship)
        menu.selected_ship = menu.cell_selected_ship = None


def action_on_mouse_alone(menu):
    menu.draw_text('Играть с компьютером',
                   menu.buttons.alone_button.rect.bottomleft,
                   menu.theme.value['main_colour'],
                   menu.theme.value['background_colour'])


def action_on_mouse_with_friend(menu):
    menu.draw_text('Играть с другом',
                   menu.buttons.with_friend_button.rect.bottomleft,
                   menu.theme.value['main_colour'],
                   menu.theme.value['background_colour'])


def action_theme(menu):
    if menu.theme == Theme.light:
        menu.theme = Theme.dark
    else:
        menu.theme = Theme.light
    selected_colour = menu.theme.value['selected_ship_colour']
    menu.buttons = Buttons(menu.theme)
    if not menu.sea_battle: return
    menu.sea_battle.theme = menu.theme
    for ship in menu.sea_battle.player1.grid.ships.ships:
        if menu.selected_ship and ship == menu.selected_ship:
            ship.colour = menu.theme.value['selected_ship_colour']
        elif ship.colour != 'red':
            ship.colour = menu.theme.value['ship_colour']
    for ship in menu.sea_battle.player2.grid.ships.ships:
        if menu.selected_ship and ship == menu.selected_ship:
            ship.colour = menu.theme.value['selected_ship_colour']
        elif ship.colour != 'red':
            ship.colour = menu.theme.value['ship_colour']


class Buttons:
    def __init__(self, theme: Theme):
        self.resume_button = Button(0, 0, 'button_resume.png', theme,1,
                                    action_resume)
        self.alone_button = Button(0, 0, 'computer.png', theme,3, action_alone,
                                   action_on_mouse_alone)
        self.with_friend_button = Button(0, 0, 'friend.png', theme, 3,
                                         action_with_friend,
                                         action_on_mouse_with_friend)
        self.play_button = Button(0, 0, 'play.png', theme, 2, action_play)
        self.auto_button = Button(0, 0, 'auto.png', theme,2, action_auto)
        self.back_button = Button(0, 0, 'back.png', theme, 2, action_back)
        self.rotate_button = Button(0, 0, 'reset.png', theme,1, action_rotate)
        self.done_button = Button(0, 0, 'done.png', theme,1, action_done)
        self.theme_button = Button(0, 0, 'theme.png', theme,1, action_theme)
        self.plus_x_button = Button(0, 0, 'plus.png', theme, 1, action_plus_x)
        self.minus_x_button = Button(0, 0, 'minus.png', theme, 1, action_minus_x)
        self.plus_y_button = Button(0, 0, 'plus.png', theme, 1, action_plus_y)
        self.minus_y_button = Button(0, 0, 'minus.png', theme, 1, action_minus_y)

