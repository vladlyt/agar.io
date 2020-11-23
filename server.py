import socketserver
import pickle
from collections import namedtuple

from enums import MessageEnum, MOVE_SIZE
from game import Board, Player

BOARD_BOUNDS = (1000, 1000)

Message = namedtuple('Message', ['type', 'data'])

board = Board(bounds=BOARD_BOUNDS)
board.fill_cells((BOARD_BOUNDS[0] + BOARD_BOUNDS[1]) // 4)
clients = {}


class UDPHandler(socketserver.BaseRequestHandler):

    def send_data(self, data):
        socket = self.request[1]
        socket.sendto(pickle.dumps(data), self.client_address)

    def get_message(self):
        raw_message = pickle.loads(self.request[0])
        return Message(raw_message['type'], raw_message.get('data'))

    def handle(self):
        global clients
        global board

        message = self.get_message()
        if message.type == MessageEnum.CONNECT:
            print(f'New player {message.data} is connected!')
            new_player = Player.random_player(name=message.data, bounds=BOARD_BOUNDS)
            self.send_data(new_player.uuid)
            clients[self.client_address] = new_player
            board.add_player(new_player)
        elif message.type == MessageEnum.UPDATE:
            player = clients[self.client_address]
            xv = message.data['xv'] if abs(message.data['xv']) <= MOVE_SIZE else 0
            yv = message.data['yv'] if abs(message.data['yv']) <= MOVE_SIZE else 0
            board.move_player(player, xv, yv)
            board.update()
            self.send_data(board.get_player_info(player.x, player.y))


class Server:

    def __init__(self, host='localhost', port=8889):
        self.host = host
        self.port = port

    def serve(self):
        with socketserver.UDPServer((self.host, self.port), UDPHandler) as srv:
            print('Running server at {}:{}'.format(self.host, self.port))
            srv.serve_forever()


if __name__ == '__main__':
    Server().serve()
