from typing import TypeVar
from gale.factory import Factory
from src.powerups.PowerUp import PowerUp


class Cannon(PowerUp):

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, 1)
        self.play_state = None

    def take(self, play_state: TypeVar("PlayState")) -> None:
        self.play_state = play_state
        self.play_state.fill_cannons()

        self.in_play = False