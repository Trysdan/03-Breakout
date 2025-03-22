"""
ISPPV1 2025
Study Case: Breakout

Author: Jesus Diaz
jdnieldp99@gmail.com

Power-up que activa teletransporte por los bordes durante 10 segundos.
"""
from typing import TypeVar
import pygame
from src.powerups.PowerUp import PowerUp
import settings

class TeleportEdges(PowerUp):
    """
    Power-up to cross the edges infinitely.
    """
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, 9)
        self.effect_duration = 5000
        self.effect_start_time = 0
        self.play_state_ref = None

    def take(self, play_state: TypeVar("PlayState")) -> None:
        self.play_state_ref = play_state
        self.effect_start_time = pygame.time.get_ticks()
        self.vy = 0

    def update(self, dt: float) -> None:
        if self.play_state_ref is None:
            super().update(dt)
        else:
            current_time = pygame.time.get_ticks()
            if current_time - self.effect_start_time < self.effect_duration:
                self.play_state_ref.border_bounce = False
                self._apply_teleport()
            else:
                self.play_state_ref.border_bounce = True
                self.active = False

    def _apply_teleport(self) -> None:
        for ball in self.play_state_ref.balls:
            if ball.x + ball.width < 0:
                ball.x = settings.VIRTUAL_WIDTH
            elif ball.x > settings.VIRTUAL_WIDTH:
                ball.x = -ball.width
            
            if ball.y + ball.height < 0:
                ball.y = settings.VIRTUAL_HEIGHT
            elif ball.y > settings.VIRTUAL_HEIGHT:
                ball.y = -ball.height

    def render(self, surface: pygame.Surface) -> None:
        if self.play_state_ref is None:
            super().render(surface)