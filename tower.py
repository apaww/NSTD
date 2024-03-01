import pygame
from settings import *
import math


class Tower(pygame.sprite.Sprite):
    def __init__(self, pos, group, name):
        super().__init__(group)
        self.name = name
        self.frames = []
        for i in range(9):
            frame = pygame.image.load(
                f'./assets/images/towers/{self.name}{i + 1}.png').convert_alpha()
            frame = pygame.transform.scale(frame, (64, 64))
            self.frames.append(frame)
        frame = pygame.image.load(
            f'./assets/images/towers/{self.name}{1}.png').convert_alpha()
        frame = pygame.transform.scale(frame, (64, 64))
        self.frames.append(frame)
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.cooldown = 1500
        self.last_animation = pygame.time.get_ticks()

        self.og_image = self.frames[self.frame_index]
        self.angle = 0
        self.tile = pos
        self.pos = ((self.tile[0] + 0.5) * TILE_SIZE,
                    (self.tile[1] + 0.5) * TILE_SIZE)
        self.image = pygame.transform.rotate(self.og_image, self.angle)
        self.rect = self.image.get_rect(center=self.pos)
        self.cooldown = 1

    def update(self, dt, enemies_sprites):
        if not pygame.time.get_ticks() - self.last_animation > self.cooldown:
            return
        enemy = pygame.sprite.spritecollideany(self, enemies_sprites)
        if enemy:
            if self.cooldown == 1:
                enemy.get_damage()
            self.play_animation(enemy.get_rect().center)

    def get_rect(self):
        return self.rect

    def get_surf(self):
        return self.image

    def play_animation(self, pos):
        self.cooldown = 0
        self.og_image = self.frames[self.frame_index]
        self.image = pygame.transform.rotate(self.og_image, self.angle)
        if pygame.time.get_ticks() - self.update_time > ANIMATION_DELAY:
            self.update_time = pygame.time.get_ticks()
            self.frame_index = self.frame_index + \
                1 if self.frame_index + 1 < len(self.frames) else 0
            if self.frame_index == 0:
                self.last_animation = pygame.time.get_ticks()
                self.cooldown = 1
            self.lookAt(pos)

    def lookAt(self, pos):
        delta_vector = pos - pygame.math.Vector2(self.rect.center)
        self.angle = (180 / math.pi) * \
            math.atan2(-delta_vector.x, -delta_vector.y)
        self.image = pygame.transform.rotozoom(self.og_image, self.angle, 1)
        current_pos = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = current_pos
