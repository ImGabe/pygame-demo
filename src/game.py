import pygame

from colors import RED, BLACK, WHITE
from constant import CAPTION, FPS, HEIGHT, WIDTH

from sound import SoundManager

from gameState import GameState
from obstacle import Obstacle
from player import Player


class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        pygame.display.set_caption(CAPTION)
        # pygame.display.set_icon(pygame.image.load("icon.png"))

        self.running = True
        self.pause = False

        self.screen = pygame.display.set_mode(
            (WIDTH, HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF
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
        self.obstacles = []

        # Sprite groups
        self.obstacles_group = pygame.sprite.Group()
        self.all_sprite = pygame.sprite.Group()

    def on_init(self):
        self.pause = True

        # Add player to sprite group
        self.all_sprite.add(self.player)

        # Add obstacle to sprite group
        for _ in range(20):
            obstacle = Obstacle()

            self.obstacles.append(obstacle)
            self.all_sprite.add(obstacle)
            self.obstacles_group.add(obstacle)

    def on_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
                self.pause = False

            if event.key == pygame.K_p:
                self.pause = not self.pause

            if event.key == pygame.K_RETURN and self.pause:
                self.pause = False

        if event.type == pygame.QUIT:
            self.running = False
            self.pause = False

    def on_loop(self):
        # update all sprites
        self.all_sprite.update(self.dt)
        self.game_state.update()

        # Check collision
        blocks_hit_list = pygame.sprite.spritecollide(
            self.player, self.obstacles_group, True
        )

        for _ in blocks_hit_list:
            self.sound_manager.collision()
            self.pause = True

            self.on_save()
            self.on_restart()

    def on_render(self):
        # fill the screen with black
        self.screen.fill(BLACK)

        # draw the scoreboard
        text = f"Points: {self.game_state._points}"
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

    def on_pause(self):
        # draw pause text
        pause_text = "Aperte Enter para começar"
        pause_text_surface = self.font.render(pause_text, True, WHITE)

        score_text = f"Highscore: {self.game_state.highest_score}"
        score_text_surface = self.font.render(score_text, True, WHITE)

        self.screen.blit(
            pause_text_surface,
            (
                (WIDTH - pause_text_surface.get_width()) // 2,
                (HEIGHT - pause_text_surface.get_height()) // 2,
            ),
        )

        self.screen.blit(
            score_text_surface,
            (
                (WIDTH - score_text_surface.get_width()) // 2,
                (HEIGHT - score_text_surface.get_height()) // 4,
            ),
        )

        while self.pause:
            for event in pygame.event.get():
                self.on_event(event)

            pygame.display.update()
            self.clock.tick(15)

    def on_restart(self):
        self.game_state.restart()
        self.player.restart()

        self.all_sprite.empty()
        self.obstacles_group.empty()

        self.obstacles.clear()

        self.on_init()

    def on_save(self):
        self.game_state.update_highest_score()
        self.game_state.save_data()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() is False:
            self.running = False

        # Main loop
        while self.running:
            for event in pygame.event.get():
                self.on_event(event)

            self.on_pause()
            self.on_loop()
            self.on_render()

            self.clock.tick(self.fps)

        self.on_cleanup()
