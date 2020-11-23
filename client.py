import socket
import pickle
import time

import pygame

from view import Menu
from enums import MessageEnum, MOVE_SIZE
from view import View, Camera


class Connection:

    def __init__(self, screen):
        self.screen = screen
        self.player_uuid = None
        self.host = None
        self.port = None
        self.server_address = None
        self.xv = self.yv = 0

    def get_sock(self):
        return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_data(self, data, sock):
        sock.sendto(pickle.dumps(data), (self.host, self.port))
        return sock

    def get_data(self, sock, buffer_size):
        return pickle.loads(sock.recv(buffer_size))

    def update_xv_yv(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.xv = -MOVE_SIZE
            elif event.key == pygame.K_RIGHT:
                self.xv = MOVE_SIZE
            elif event.key == pygame.K_UP:
                self.yv = MOVE_SIZE
            elif event.key == pygame.K_DOWN:
                self.yv = -MOVE_SIZE
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and self.xv == -MOVE_SIZE:
                self.xv = 0
            elif event.key == pygame.K_RIGHT and self.xv == MOVE_SIZE:
                self.xv = 0
            elif event.key == pygame.K_UP and self.yv == MOVE_SIZE:
                self.yv = 0
            elif event.key == pygame.K_DOWN and self.yv == -MOVE_SIZE:
                self.yv = 0

    def connect_to_game(self, get_attrs):
        attrs = get_attrs()
        self.server_address = attrs['server_address']
        self.host, port = self.server_address.split(':')
        self.port = int(port)

        try:
            sock = self.get_sock()
            self.send_data(
                {
                    'type': MessageEnum.CONNECT,
                    'data': attrs['name'],
                },
                sock,
            )
            self.player_uuid = self.get_data(sock, 2 ** 12)
            print(f'Got player_uuid: {self.player_uuid}')

            view = View(self.screen, Camera(0, 0, View.SCREEN_WIDTH, View.SCREEN_HEIGHT), None)
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()
                    self.update_xv_yv(event)
                self.send_data(
                    {
                        'type': MessageEnum.UPDATE,
                        'data': {
                            'xv': self.xv,
                            'yv': self.yv,
                        },
                    },
                    sock,
                )

                board = self.get_data(sock, 2 ** 16)
                for player in board.players:
                    if player.uuid == self.player_uuid:
                        view.set_player(player)
                        break
                else:
                    print("Player was killed!")
                    return
                view.render_board(board)
                time.sleep(1 / 30)
        except socket.timeout:
            print('Server timeout')


class Client:
    BACKGROUND_COLOR = (40, 0, 40)
    MENU_WIDTH = View.SCREEN_WIDTH * 0.9
    MENU_HEIGHT = View.SCREEN_HEIGHT * 0.9

    def __init__(self):
        socket.setdefaulttimeout(2)

        pygame.init()
        pygame.display.set_caption('Multiplayer Agar.io')

        self.screen = pygame.display.set_mode((View.SCREEN_WIDTH, View.SCREEN_HEIGHT))

        connection = Connection(self.screen)
        self.menu = Menu(self.MENU_WIDTH, self.MENU_HEIGHT)
        # set callback
        self.menu.update_start_menu(connection.connect_to_game)
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()

            self.screen.fill(self.BACKGROUND_COLOR)

            if self.menu.get_main_menu().is_enabled():
                self.menu.get_main_menu().draw(self.screen)
            self.menu.get_main_menu().update(events)
            pygame.display.flip()
            self.clock.tick(30)


if __name__ == '__main__':
    Client().run()
