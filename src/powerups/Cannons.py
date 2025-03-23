import pygame

import settings
from src.states import PlayState
from gale.factory import Factory
from src.powerups.Projectile import Projectile
from gale.input_handler import InputData
from typing import TypeVar

class Cannons:
    
    #We use paddle as a parameter to get its position
    def __init__(self, paddle_x : int, paddle_y : int, play_state: PlayState) -> None: 

        #super().__init__(paddle_x, paddle_y, 1)
        self.projectile_factory = Factory(Projectile)
        self.width = 32
        self.height = 52  
        self.texture = settings.TEXTURES["cannons"]
        self.frame = settings.FRAMES["cannons"][0]
        self.paddlex = paddle_x
        self.paddley = paddle_y
        self.play_state = play_state
    
    def take(self, play_state: TypeVar("PlayState"))-> None:
        self.effect_start_time = pygame.time.get_ticks()/ 1000
 
    def shoot_projectiles(self):
         
        projectile = self.projectile_factory.create(self.paddlex, self.paddley)
        projectile.vy = settings.PROJECTILE_SPEED
        self.play_state.projectiles.append(projectile)

    def update(self):
    
        for projectile in self.projectiles:
            projectile.update() 

        self.projectiles = [p for p in self.projectiles if p.is_on_screen()]

    def render(self, surface: pygame.Surface) -> None:
        
         surface.blit(
            self.texture, (self.x, self.y), self.frame
        )
        
