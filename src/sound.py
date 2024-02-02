import pygame


class SoundManager:
    def __init__(self):
        self.collision_effect = pygame.mixer.Sound("./assets/sounds/collision.mp3")

    def collision(self):
        self.collision_effect.play()
