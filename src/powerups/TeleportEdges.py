"""
ISPPV1 2025
Study Case: Breakout

Author: Jesus Diaz
jdnieldp99@gmail.com

This file contains the specialization of PowerUp to cross the edges infinitely.
"""
from typing import TypeVar
import pygame
from src.powerups.PowerUp import PowerUp
import settings

class TeleportEdges(PowerUp):
    """
    Power-up to cross the edges infinitely.
    """
    #Avoid multiple instances of the same active power-up, I reset the timer.
    effect_final_time = 0
    effect_active = False
    
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, 9)
        self.effect_duration = 5
        self.play_state_ref = None
        self.taken = False

    def take(self, play_state: TypeVar("PlayState")) -> None:
        if not self.taken: 
            self.play_state_ref = play_state
            current_time = (pygame.time.get_ticks() / 1000)
            TeleportEdges.effect_final_time = current_time + self.effect_duration
            self.vy = 0        
            if TeleportEdges.effect_active:
                self.active = False
            TeleportEdges.effect_active = True
        self.taken = True

    def update(self, dt: float) -> None:
        if self.play_state_ref is None:
            super().update(dt)
        else:
            current_time = (pygame.time.get_ticks() / 1000)            
            if current_time < TeleportEdges.effect_final_time:
                self.play_state_ref.border_bounce = False
                self._apply_teleport()
            else:
                self.play_state_ref.border_bounce = True
                self.active = False
                TeleportEdges.effect_active = False

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

    def _draw_border_effect(self, surface: pygame.Surface) -> None:
        border_color = (0, 255, 0)
        border_width = 1

        pygame.draw.rect(
            surface,
            border_color,
            (0, 0, settings.VIRTUAL_WIDTH, border_width))
        
        pygame.draw.rect(
            surface,
            border_color,
            (0, settings.VIRTUAL_HEIGHT - border_width, settings.VIRTUAL_WIDTH, border_width))
        
        pygame.draw.rect(
            surface,
            border_color,
            (0, 0, border_width, settings.VIRTUAL_HEIGHT))
        
        pygame.draw.rect(
            surface,
            border_color,
            (settings.VIRTUAL_WIDTH - border_width, 0, border_width, settings.VIRTUAL_HEIGHT))

    def render(self, surface: pygame.Surface) -> None:
        if self.play_state_ref is None:
            super().render(surface)
        else:
            current_time = (pygame.time.get_ticks() / 1000)            
            if current_time < TeleportEdges.effect_final_time:
                self._draw_border_effect(surface)