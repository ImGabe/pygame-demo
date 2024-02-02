import random

import pygame

from constant import HEIGHT, WIDTH
from colors import RED


class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((random.randint(30, 150), random.randint(20, 30)))
        self.image.fill(RED)

        self.rect = self.image.get_rect()

        self.reset_pos()

    def update(self, dt):
        if self.rect is None:
            raise ValueError('For some reason the rect not exist')

        self.rect.x -= self.speed * dt

        if self.rect.x < 0:
            self.reset_pos()

    def reset_pos(self):
        if self.rect is None:
            raise ValueError('For some reason the rect not exist')
        
        self.rect.x = random.randint(WIDTH, WIDTH * 2)
        self.rect.y = random.randint(0, HEIGHT - 10)

        self.speed = random.randint(300, 500)
