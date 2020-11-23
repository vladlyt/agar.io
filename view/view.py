import time

import pygame


class View:
    TEXT_COLOR = (50, 50, 50)
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 800

    def __init__(self, screen, camera, player):
        self.camera = camera
        self.screen = screen
        self.player = player
        self.font = pygame.font.Font(pygame.font.get_default_font(), 18)
        self.hud_srf = pygame.Surface((1, 1), pygame.SRCALPHA)

    def set_player(self, player):
        self.player = player

    def render_text(self, surface, text, x, y, color=TEXT_COLOR, align_center=False):
        text_srf = self.font.render(text, True, color)
        if align_center:
            x -= text_srf.get_width() // 2
            y -= text_srf.get_height() // 2
        surface.blit(text_srf, (x, y))

    def render_new_round(self):
        self.render_text(
            self.screen,
            "NEW ROUND HAS BEEN STARTED",
            self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 * 0.1,
            (225, 0, 0),
            align_center=True,
        )

    def render_hud(self, players, x, y):
        self.render_item(
            10, self.SCREEN_HEIGHT - 50,
            (f'Your score: {self.player.radius}',),
            x, y,
        )
        hud_info = ['Leaders']
        for i, player in enumerate(sorted(
                players,
                key=lambda p: p.radius,
                reverse=True,
        )[:10], start=1):
            hud_info.append(f'{i}. {player.name}')
        self.render_item(
            self.SCREEN_WIDTH - 120, 10,
            hud_info,
            x, y,
        )

    def render_item(self, x_pos, y_pos, hud_info, x, y):
        max_available_width = max(map(lambda i: self.font.size(i)[0], hud_info))
        height = self.font.get_height()
        item_size = (
            max_available_width + 2 * x,
            height * len(hud_info) + 2 * y,
        )
        srf = pygame.transform.scale(self.hud_srf, item_size)
        for i, hud_text in enumerate(hud_info):
            self.render_text(
                srf,
                hud_text,
                x,
                y + height * i,
            )
        self.screen.blit(srf, (x_pos, y_pos))

    def render_player(self, player):
        pygame.draw.circle(
            self.screen,
            player.color,
            self.camera.adjust(player.x, player.y),
            player.radius,
        )

    def render_cell(self, cell):
        pygame.draw.circle(
            self.screen,
            cell.color,
            self.camera.adjust(cell.x, cell.y),
            cell.radius,
        )

    def render_board(self, board):
        self.camera.set_to_center(self.player.x, self.player.y)
        self.screen.fill((255, 255, 255))

        if time.time() - board.start_round_time <= 10:
            self.render_new_round()
        self.render_hud(board.players, 10, 10)

        for cell in board.cells:
            self.render_cell(cell)

        for player in board.players:
            self.render_player(player)
            self.render_text(
                self.screen,
                player.name,
                *self.camera.adjust(player.x, player.y),
                align_center=True,
            )

        pygame.display.flip()
