import pygame
import json
from settings import *
from enemy import Enemy
from tower import Tower
from loader import Board
from levels.config import WAVES
from random import randint


class Level:
    def __init__(self, level, board, shop):
        self.display_surf = pygame.display.get_surface()
        self.level = level

        self.enemies_group = pygame.sprite.Group()

        self.board = board
        self.shop = shop
        self.setup()
        self.wave = 0
        self.running = 0

    def setup(self):
        self.image = pygame.image.load(
            f'./levels/{self.level}/map.png').convert_alpha()

        self.board.load()
        self.board.fill_board()
        self.waypoints = self.board.get_waypoints()

    def draw(self):
        self.display_surf.blit(self.image, (0, 0))

    def run(self, dt):
        self.draw()
        if not self.enemies_group and self.running:
            self.wave += 1
            self.running = 0
        if not self.running:
            font = pygame.font.Font('./assets/fonts/Silver.ttf', 100)
            start_game_surf = font.render(
                'Press space to start wave', False, '#4c3630')
            start_game_rect = start_game_surf.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.display_surf.blit(start_game_surf, start_game_rect)
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                self.start_wave()
        # pygame.draw.lines(self.display_surf, 'grey0', False, self.waypoints)

    def get_enemies(self):
        return self.enemies_group

    def start_wave(self):
        print(WAVES[self.level - 1][self.wave])
        for j in range(len(WAVES[self.level - 1][self.wave])):
            for i in range(0, len(WAVES[self.level - 1][self.wave][j]), 3):
                self.enemy1 = Enemy(
                    self.waypoints, self.enemies_group, WAVES[self.level - 1][self.wave][j][i], randint(100, 400), WAVES[self.level - 1][self.wave][j][i + 1], WAVES[self.level - 1][self.wave][j][i + 2], self.shop)
        self.running = 1

    def get_wave(self):
        return self.wave

    def get_level(self):
        return self.level
