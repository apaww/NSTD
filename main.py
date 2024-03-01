import pygame
import sys
from settings import *
from level import Level
from inventory import Inventory
from loader import Board
from levels.config import WAVES


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (SCREEN_WIDTH, SCREEN_HEIGHT + HOTBAR))
        pygame.display.set_caption(
            'Nothing Special Tower Defense')
        icon_surf = pygame.image.load(
            './assets/images/icon.png').convert_alpha()
        pygame.display.set_icon(icon_surf)
        self.clock = pygame.time.Clock()
        self.board = Board(1)
        self.inventory = Inventory(self.board)
        self.level = Level(1, self.board, self.inventory)
        self.money = 0
        self.killed = 0
        self.wave = 0
        bg_music = pygame.mixer.Sound('./assets/audio/music.wav')
        bg_music.set_volume(0.05)
        bg_music.play(loops=-1)

    def run(self):
        state = 'start'
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            dt = self.clock.tick() / 1000
            self.screen.fill('#dcb98a')
            if state == 'game':
                enemies_group = self.level.get_enemies()
                towers_group = self.inventory.get_towers()

                if self.level.get_wave() == len(WAVES[self.level.get_level() - 1]):
                    state = 'won'
                    self.money = self.inventory.get_money()
                    self.killed = self.inventory.get_killed()
                    self.wave = self.level.get_wave()
                    enemies_group.empty()
                    towers_group.empty()

                self.level.run(dt)
                enemies_group.draw(self.screen)
                enemies_group.update(dt)
                self.inventory.run(dt)
                towers_group.draw(self.screen)
                towers_group.update(dt, enemies_group)
                if self.inventory.get_hp() <= 0:
                    state = 'lose'
                    self.money = self.inventory.get_money()
                    self.killed = self.inventory.get_killed()
                    self.wave = self.level.get_wave()
                    enemies_group.empty()
                    towers_group.empty()
                if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    state = 'pause'
                    self.money = self.inventory.get_money()
                    self.killed = self.inventory.get_killed()
                    self.wave = self.level.get_wave() + 1
            elif state == 'start':
                level = 1
                font = pygame.font.Font('./assets/fonts/Silver.ttf', 100)
                start_game_surf = font.render(
                    'Press number of level to start', False, '#4c3630')
                start_game_rect = start_game_surf.get_rect(
                    center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                self.screen.blit(start_game_surf, start_game_rect)
                start_game_surf2 = font.render(
                    '(3 levels are available)', False, '#4c3630')
                start_game_rect2 = start_game_surf2.get_rect(
                    center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 110))
                self.screen.blit(start_game_surf2, start_game_rect2)
                if pygame.key.get_pressed()[pygame.K_1]:
                    state = 'game'
                    level = 1
                elif pygame.key.get_pressed()[pygame.K_2]:
                    state = 'game'
                    level = 2
                elif pygame.key.get_pressed()[pygame.K_3]:
                    state = 'game'
                    level = 3
                self.board = Board(level)
                self.inventory = Inventory(self.board)
                self.level = Level(level, self.board, self.inventory)
            elif state == 'pause':
                font = pygame.font.Font('./assets/fonts/Silver.ttf', 100)
                pause_game_surf = font.render(
                    'Game paused', False, '#4c3630')
                pause_game_rect = pause_game_surf.get_rect(
                    center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
                self.screen.blit(pause_game_surf, pause_game_rect)
                font2 = pygame.font.Font('./assets/fonts/Silver.ttf', 70)
                pause_game_surf2 = font2.render(
                    'press \'space\' to resume game', False, '#4c3630')
                pause_game_rect2 = pause_game_surf2.get_rect(
                    center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 100))
                self.screen.blit(pause_game_surf2, pause_game_rect2)
                pause_game_surf3 = font2.render(
                    'press \'backspace\' to exit to the main menu', False, '#4c3630')
                pause_game_rect3 = pause_game_surf3.get_rect(
                    center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 200))
                self.screen.blit(pause_game_surf3, pause_game_rect3)
                font_results = pygame.font.Font(
                    './assets/fonts/Silver.ttf', 50)
                results_game_surf = font_results.render(
                    f'Wave: {self.wave} | Money: {self.money} | Killed enemies: {self.killed}', False, '#4c3630')
                results_game_rect = results_game_surf.get_rect(
                    center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 400))
                self.screen.blit(results_game_surf, results_game_rect)
                if pygame.key.get_pressed()[pygame.K_SPACE]:
                    state = 'game'
                elif pygame.key.get_pressed()[pygame.K_BACKSPACE]:
                    state = 'start'
            elif state == 'lose':
                font = pygame.font.Font('./assets/fonts/Silver.ttf', 100)
                lost_game_surf = font.render(
                    'You lost ;_;', False, '#4c3630')
                lost_game_rect = lost_game_surf.get_rect(
                    center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
                self.screen.blit(lost_game_surf, lost_game_rect)
                font2 = pygame.font.Font('./assets/fonts/Silver.ttf', 70)
                exit_game_surf2 = font2.render(
                    'press \'backspace\' to exit to the main menu', False, '#4c3630')
                exit_game_rect2 = exit_game_surf2.get_rect(
                    center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 100))
                self.screen.blit(exit_game_surf2, exit_game_rect2)
                font_results = pygame.font.Font(
                    './assets/fonts/Silver.ttf', 50)
                results_game_surf = font_results.render(
                    f'Wave: {self.wave} | Money: {self.money} | Killed enemies: {self.killed}', False, '#4c3630')
                results_game_rect = results_game_surf.get_rect(
                    center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 400))
                self.screen.blit(results_game_surf, results_game_rect)
                if pygame.key.get_pressed()[pygame.K_BACKSPACE]:
                    state = 'start'
            elif state == 'won':
                font = pygame.font.Font('./assets/fonts/Silver.ttf', 100)
                lost_game_surf = font.render(
                    'You won! *^____^*', False, '#4c3630')
                lost_game_rect = lost_game_surf.get_rect(
                    center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
                self.screen.blit(lost_game_surf, lost_game_rect)
                font2 = pygame.font.Font('./assets/fonts/Silver.ttf', 70)
                exit_game_surf2 = font2.render(
                    'press \'backspace\' to exit to the main menu', False, '#4c3630')
                exit_game_rect2 = exit_game_surf2.get_rect(
                    center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 100))
                self.screen.blit(exit_game_surf2, exit_game_rect2)
                font_results = pygame.font.Font(
                    './assets/fonts/Silver.ttf', 50)
                results_game_surf = font_results.render(
                    f'Wave: {self.wave} | Money: {self.money} | Killed enemies: {self.killed}', False, '#4c3630')
                results_game_rect = results_game_surf.get_rect(
                    center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 400))
                self.screen.blit(results_game_surf, results_game_rect)
                if pygame.key.get_pressed()[pygame.K_BACKSPACE]:
                    state = 'start'
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
