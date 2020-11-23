from functools import partial

import pygame_menu


class Menu:

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.theme = pygame_menu.themes.THEME_SOLARIZED.copy()
        self.theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_ADAPTIVE
        self.theme.widget_selection_effect = pygame_menu.widgets.NoneSelection()

        self.start_menu = pygame_menu.Menu(
            theme=self.theme,
            height=self.height,
            width=self.width,
            onclose=pygame_menu.events.RESET,
            title='Start',
        )
        self.main_menu = pygame_menu.Menu(
            theme=self.theme,
            height=self.height,
            width=self.width,
            onclose=pygame_menu.events.EXIT,
            title='Main menu',
        )

        self.init_widgets()

    def init_widgets(self):
        self.update_start_menu(lambda *args: None)

        self.main_menu.add_button(self.start_menu.get_title(), self.start_menu)
        self.main_menu.add_button('Exit', pygame_menu.events.EXIT)

    def update_start_menu(self, connect_callback):
        self.start_menu.clear()

        self.start_menu.add_text_input(
            'Your name: ',
            default='kek',
            maxwidth=20,
            textinput_id='name',
            input_underline='_',
        )
        self.start_menu.add_text_input(
            'Server address: ',
            default='localhost:8889',
            maxwidth=20,
            textinput_id='server_address',
            input_underline='_',
        )
        self.start_menu.add_vertical_margin(25)
        self.start_menu.add_button(
            'Connect',
            partial(
                connect_callback,
                self.start_menu.get_input_data,
            ),
        )
        self.start_menu.add_button('Back', pygame_menu.events.RESET)

    def get_main_menu(self):
        return self.main_menu
