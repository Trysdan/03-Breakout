import pygame 

import settings 
from gale.factory import Factory
from src.Paddle import Paddle
from typing import Any, Tuple, Optional

class Projectile:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y 
        self.width = 16
        self.height = 16

        self.vx = 0 
        self.vy = settings.PROJECTILE_SPEED

        self.texture = settings.TEXTURES["cannons"]
        self.frame = settings.FRAMES["projectile"][8]

    #dimensions of projectile
    def get_collision_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def collides(self, another: Any) -> bool:
        return self.get_collision_rect().colliderect(another.get_collision_rect())
    
    def update(self, dt: float) -> None:
        self.y += self.vy * dt

    def solve_world_boundaries(self) -> None:
        r = self.get_collision_rect()

        if r.top > settings.VIRTUAL_HEIGHT:
            settings.SOUNDS["hurt"].play()
            self.in_play = False

    def get_intersection(r1: pygame.Rect, r2: pygame.Rect) -> Optional[Tuple[int, int]]:
        
        if r1.x > r2.right or r1.right < r2.x or r1.bottom < r2.y or r1.y > r2.bottom:
            # There is no intersection
            return None

        # Compute x shift
        if r1.centerx < r2.centerx:
            x_shift = r2.x - r1.right
        else:
            x_shift = r2.right - r1.x

        # Compute y shift
        if r1.centery < r2.centery:
            y_shift = r2.y - r1.bottom
        else:
            y_shift = r2.bottom - r1.y

        return (x_shift, y_shift)

    def render(self, surface):
        surface.blit(
            self.texture, (self.x - 30, self.y - 30), self.frame
        )


        


