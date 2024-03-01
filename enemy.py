from typing import Any
import pygame
from settings import *
import math


class Enemy(pygame.sprite.Sprite):
    def __init__(self, waypoints, group, name, speed, health, coins, shop):
        super().__init__(group)
        self.waypoints = waypoints
        self.pos = pygame.math.Vector2(self.waypoints[0])
        self.target_waypoint = 1
        self.name = name
        frame_1 = pygame.image.load(
            f'./assets/images/enemies/{self.name}.png').convert_alpha()
        frame_1 = pygame.transform.scale(frame_1, (160, 160))
        self.frames = [frame_1]
        self.frame_index = 0

        self.og_image = self.frames[self.frame_index]
        self.angle = -180

        self.image = pygame.transform.rotate(self.og_image, self.angle)
        self.rect = self.image.get_rect(center=self.pos)

        self.speed = speed
        self.health = health
        self.coins = coins

        self.shop = shop

    def move(self, dt):
        if self.target_waypoint < len(self.waypoints):
            self.target = pygame.math.Vector2(
                self.waypoints[self.target_waypoint])
            self.movement = self.target - self.pos
        else:
            self.kill()
            self.shop.get_damage()

        distance = self.movement.length()
        if distance >= self.speed * dt:
            self.pos += self.movement.normalize() * self.speed * dt
        else:
            if distance != 0:
                self.pos += self.movement.normalize() * distance * dt
            self.target_waypoint += 1
        self.rect.center = self.pos  # type: ignore

    def rotate(self):
        distance = self.target - self.pos
        self.angle = math.degrees(math.atan2(-distance[1], distance[0])) - 180
        self.image = pygame.transform.rotate(self.og_image, self.angle)
        self.rect = self.image.get_rect(center=self.pos)

    def update(self, dt):
        self.move(dt)
        self.rotate()

    def get_rect(self):
        return self.rect

    def get_damage(self):
        self.health -= 100
        if self.health <= 0:
            self.kill()
            self.shop.get_coins(self.coins)
            self.shop.killed += 1
