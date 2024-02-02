class GameState:
    def __init__(self):
        self.points = 0

    def update(self):
        self.points += 1

    def restart(self):
        self.points = 0
