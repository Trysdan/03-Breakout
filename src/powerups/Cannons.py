import pygame

import settings
from src.Paddle import Paddle
from gale.factory import Factory
from src.powerups.PowerUp import PowerUp
from src.powerups.Projectile import Projectile
from gale.input_handler import InputData

class Cannons(PowerUp):
    
    #We use paddle as a parameter to get its position
    def __init__(self, paddle: Paddle) -> None: 
        super().__init__(paddle.x, paddle.y, 0)
        self.cannons_factory = Factory(Projectile)
        self.width = 32
        self.height = 52

        self.paddle = paddle       
        self.texture = settings.TEXTURES["cannons"]

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "shoot" and input_data.pressed:
            settings.SOUNDS["paddle_hit"].play()
            self.shoot_projectiles()

    def shoot_projectiles(self):
       
        left_cannon_x = self.paddle.x
        left_cannon_y = self.paddle.y + self.paddle.height // 2 - self.height // 2
        
        right_cannon_x = self.paddle.x + self.paddle.width - self.width
        right_cannon_y = self.paddle.y + self.paddle.height // 2 - self.height // 2
         
        left_projectile = self.cannons_factory.create(left_cannon_x, left_cannon_y)
        right_projectile = self.cannons_factory.create(right_cannon_x, right_cannon_y)
        
        left_projectile.vy = settings.PROJECTILE_SPEED
        right_projectile.vx = settings.PROJECTILE_SPEED

        self.projectiles.append(left_projectile)
        self.projectiles.append(right_projectile)

    def update(self):
    
        for projectile in self.projectiles:
            projectile.update() 

        self.projectiles = [p for p in self.projectiles if p.is_on_screen()]

    def render(self, surface: pygame.Surface) -> None:
        
        left_cannon_x = self.paddle.x
        left_cannon_y = self.paddle.y + self.paddle.height // 2 - self.height // 2
        
        right_cannon_x = self.paddle.x + self.paddle.width - self.width
        right_cannon_y = self.paddle.y + self.paddle.height // 2 - self.height // 2
        
        surface.blit(
            self.texture, (left_cannon_x, left_cannon_y), settings.FRAMES["cannons"])
        
        surface.blit(
            self.texture, (right_cannon_x, right_cannon_y), settings.FRAMES["cannons"])
        
        for projectile in self.projectiles:
            projectile.render(surface) 