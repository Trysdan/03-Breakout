from typing import TypeVar, Any
import pygame
import settings

class Bullet:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.width = 9
        self.height = 9
        self.vy = -200
        self.active = True
        self.texture = settings.TEXTURES["bullet"]

    def get_collision_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self, dt: float, brickset: Any) -> None:
        self.y += self.vy * dt

        if self.active:
            for brick in brickset.bricks.values():
                if not brick.broken and self.collides(brick):
                    brick.hit()
                    self.active = False
                    break

        if self.y + self.height < 0:
            self.active = False

    def collides(self, another: Any) -> bool:
        return self.get_collision_rect().colliderect(another.get_collision_rect())

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(self.texture, (self.x, self.y))