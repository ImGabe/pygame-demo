import pygame

from colors import RED, BLACK
from constant import FPS, HEIGHT, WIDTH

from sound import SoundManager

from gameState import GameState
from obstacle import Obstacle
from player import Player


class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        pygame.display.set_caption("Gaming")
        # pygame.display.set_icon(pygame.image.load("icon.png"))

        self.running = True
        self.pause = False

        self.screen = pygame.display.set_mode(
            (WIDTH, HEIGHT),  pygame.HWSURFACE | pygame.DOUBLEBUF
        )
        self.size = self.width, self.height = WIDTH, HEIGHT
        self.font = pygame.font.SysFont("Comic Sans MS", 30)

        # FPS
        self.dt = 0
        self.fps = FPS

        # Clock
        self.clock = pygame.time.Clock()

        # Class
        self.sound_manager = SoundManager()
        self.game_state = GameState()
        self.player = Player()

        # Sprite groups
        self.obstacles = pygame.sprite.Group()
        self.all_sprite = pygame.sprite.Group()

    def on_init(self):
        # Add player to sprite group
        self.all_sprite.add(self.player)

        # Add obstacle to sprite group
        for _ in range(10):
            obstacle = Obstacle()

            self.all_sprite.add(obstacle)
            self.obstacles.add(obstacle)

    def on_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False

            if event.key == pygame.K_RETURN and self.pause:
                self.on_restart()

        if event.type == pygame.QUIT:
            self.running = False

    def on_loop(self):
        # update todos os sprites
        self.all_sprite.update(self.dt)
        self.game_state.update()

        # Check collision
        blocks_hit_list = pygame.sprite.spritecollide(self.player, self.obstacles, True)

        for _ in blocks_hit_list:
            self.sound_manager.collision()
            self.pause = True

    def on_render(self):
        # fill the screen with black
        self.screen.fill(BLACK)

        # draw the scoreboard
        text = f"Points: {self.game_state.points}"
        text_surface = self.font.render(text, True, RED)

        # draw the fps
        fps = f"FPS: {int(self.clock.get_fps())}"
        fps_surface = self.font.render(fps, True, RED)

        # render
        self.screen.blit(text_surface, (0, 0))
        self.screen.blit(fps_surface, (600, 0))

        self.all_sprite.draw(self.screen)

        pygame.display.flip()

        self.dt = self.clock.tick(self.fps) / 1000

    def on_restart(self):
        self.pause = False

        self.all_sprite.empty()
        self.obstacles.empty()

        self.game_state.restart()
        self.player.restart()

        self.on_init()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() is False:
            self.running = False

        # Main loop
        while self.running:
            for event in pygame.event.get():
                self.on_event(event)

            if self.pause:
                continue

            self.on_loop()
            self.on_render()

            self.clock.tick(self.fps)

        self.on_cleanup()
