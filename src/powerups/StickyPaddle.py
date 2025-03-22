from typing import TypeVar
import settings
from src.Ball import Ball
from src.powerups.PowerUp import PowerUp

class StickyPaddle(PowerUp):

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, 2)

    def take(self, play_state: TypeVar("PlayState")) -> None:
        settings.SOUNDS["paddle_hit"].stop()
        settings.SOUNDS["paddle_hit"].stop()
        paddle = play_state.paddle
        paddle.sticky = True
        self.active = False