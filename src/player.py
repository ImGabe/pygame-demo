import pygame

from constant import HEIGHT, WIDTH


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("assets/Cars/sedan.png")
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)

        self.speed = 500

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if self.rect is None:
            raise ValueError("For some reason the rect not exist")

        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed * dt

        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed * dt

    def restart(self):
        if self.rect is None:
            raise ValueError("For some reason the rect not exist")

        self.rect.center = (WIDTH // 2, HEIGHT // 2)
