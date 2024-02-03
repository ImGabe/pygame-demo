import os
import pickle

from pathlib import Path


def create_directory(directory_path):
    path = Path(directory_path)
    try:
        path.mkdir(parents=True, exist_ok=True)
    except FileExistsError:
        pass


class GameState:
    def __init__(self):
        self._points = 0
        self._highest_score = 0

        self.data_path = "data"
        self.filename = "save.pickle"

        self.file_path = os.path.join(self.data_path, self.filename)

        create_directory(self.data_path)

        self._highest_score = self.load_data()["highest_score"]

        print(self.load_data()["highest_score"])

    @property
    def highest_score(self):
        return self._highest_score

    def update_highest_score(self):
        self._highest_score = max(self._highest_score, self._points)

    def save_data(self):
        game_data = {"highest_score": self._highest_score}
        with open(self.file_path, "wb") as file:
            pickle.dump(game_data, file)

    def load_data(self):
        try:
            with open(self.file_path, "rb") as file:
                data = pickle.load(file)
                return data
        except FileNotFoundError:
            print(f"File '{self.file_path}' not found. Returning default data.")
            return {"highest_score": 0}

    def update(self):
        self._points += 1

    def restart(self):
        self._points = 0
