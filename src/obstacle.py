import os
import random

import pygame

from constant import HEIGHT, WIDTH


def get_random_file(path):
    if not os.path.exists(path) or not os.path.isdir(path):
        raise ValueError("Invalid directory path.")

    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    if not files:
        raise ValueError("No files found in the specified directory.")

    return os.path.join(path, random.choice(files))


class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.path = os.path.join("assets", "Cars")
        self.image_path = get_random_file(self.path)
        self.original_image = pygame.image.load(self.image_path)
        self.image = pygame.transform.flip(self.original_image, True, False)

        self.rect = self.image.get_rect()

        self.reset_pos()

    def update(self, dt):
        if self.rect is None:
            raise ValueError("For some reason the rect not exist")

        self.rect.x -= self.speed * dt

        if self.rect.x < (-self.rect.width):
            self.reset_pos()

    def reset_pos(self):
        if self.rect is None:
            raise ValueError("For some reason the rect not exist")

        self.rect.x = random.randint(WIDTH, WIDTH * 2)
        self.rect.y = random.randint(0, HEIGHT - 10)

        self.speed = random.randint(300, 500)
