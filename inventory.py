import pygame
import json
from settings import *
from enemy import Enemy
from tower import Tower
from loader import Board
from button import Button


class Inventory:
    def __init__(self, board):
        self.font = pygame.font.Font('./assets/fonts/Silver.ttf', 50)
        self.display_surf = pygame.display.get_surface()
        self.items = STORE
        self.store_image = pygame.image.load(
            f'./assets/images/ui/store.png').convert_alpha()
        self.placing = False
        self.money = 0
        self.board = board
        self.towers_group = pygame.sprite.Group()
        self.cursor_group = pygame.sprite.Group()
        self.cursor_tower = Tower((-100, -100), self.cursor_group, 'cat')
        self.hp = 100
        self.money = 50
        self.text = self.font.render(
            f'Money: {self.money} | Health: {self.hp}', False, 'red')
        self.killed = 0

        self.setup()

    def setup(self):
        self.store_list = []
        for i in range(len(self.items)):
            self.store_list.append(Button(
                (100 + 96 * i, SCREEN_HEIGHT + (HOTBAR / 2)), self.store_image, self.items[i][1], self.font, i))

    def run(self, dt):
        for button in self.store_list:
            pygame.draw.rect(self.display_surf, '#bd9471', button.get_rect())
            self.display_surf.blit(button.get_surf(), button.get_rect())
            button_state = button.input()
            if button_state and button.get_item() != len(self.items) - 1:
                self.placing = True
            elif button_state and button.get_item() == len(self.items) - 1:
                self.placing = False

            if self.placing:
                cursor_rect = self.cursor_tower.get_rect()
                cursor_pos = pygame.mouse.get_pos()
                cursor_rect.center = cursor_pos
                if cursor_pos[1] <= SCREEN_HEIGHT:
                    self.display_surf.blit(
                        self.cursor_tower.get_surf(), cursor_rect)
        self.input()
        self.display_score()

    def get_towers(self):
        return self.towers_group

    def input(self):
        keys = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        if keys[0] and 0 < mouse_pos[0] < SCREEN_WIDTH and 0 < mouse_pos[1] < SCREEN_HEIGHT and self.placing:
            self.create_tower(mouse_pos)

    def create_tower(self, pos):
        if self.money >= 10:
            mouse_tile = (pos[0] // TILE_SIZE, pos[1] // TILE_SIZE)
            if self.board.check(mouse_tile):
                self.towers_group.add(
                    Tower(mouse_tile, self.towers_group, 'cat'))
                self.board.take_tile(mouse_tile)
                self.money -= 10

    def display_score(self):
        self.text = self.font.render(
            f'Money: {self.money} | Health: {self.hp}', False, '#4c3630')
        self.display_surf.blit(self.text, (SCREEN_WIDTH -
                                           400, SCREEN_HEIGHT + (HOTBAR / 2)))

    def get_coins(self, coins):
        self.money += coins

    def get_damage(self):
        self.hp -= 10

    def get_hp(self):
        return self.hp

    def get_money(self):
        return self.money

    def get_killed(self):
        return self.killed
