from typing import TypeVar, Any
import pygame
from src.powerups.PowerUp import PowerUp
from src.powerups.Bullet import Bullet
import settings

class CannonsPower(PowerUp):
    """
    Adds two cannons to the paddle that shoot bullets.
    Allows 5 shots before deactivating.
    Cannons follow the paddle's movement.
    """
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, 0)
        self.shots_remaining = 5 
        self.play_state_ref = None
        self.left_cannon_pos = (0,0)        
        self.right_cannon_pos = (0,0)

    def take(self, play_state: TypeVar("PlayState")) -> None:
        self.play_state_ref = play_state
        self.vy = 0
        self._setup_cannons()

    def _setup_cannons(self):
        paddle = self.play_state_ref.paddle
        self.left_cannon_pos = (
            paddle.x - 23, 
            paddle.y - 4 
        )
        self.right_cannon_pos = (
            paddle.x + paddle.width, 
            paddle.y - 4
        )

    def update(self, dt: float) -> None:
        if self.play_state_ref is None:
            super().update(dt)
        else:
            self._setup_cannons()

    def _shoot_bullets(self):        
        if self.shots_remaining > 0 and not self.play_state_ref is None:
            left_bullet = Bullet(
                self.left_cannon_pos[0] + 11,
                self.left_cannon_pos[1]
            )
            right_bullet = Bullet(
                self.right_cannon_pos[0] + 11, 
                self.left_cannon_pos[1]
            )
            
            self.play_state_ref.bullets.append(left_bullet)
            self.play_state_ref.bullets.append(right_bullet)        
            self.shots_remaining -= 1

            if self.shots_remaining == 0:
                self.active = False

    def render(self, surface: pygame.Surface) -> None:
        if self.play_state_ref is None:
            super().render(surface)
        elif self.shots_remaining > 0:
            surface.blit(settings.TEXTURES["canon"], self.left_cannon_pos)
            surface.blit(settings.TEXTURES["canon"], self.right_cannon_pos)
