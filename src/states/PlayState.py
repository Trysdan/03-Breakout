"""
ISPPV1 2023
Study Case: Breakout

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class to define the Play state.
"""

import random

import pygame

from gale.factory import AbstractFactory
from gale.state import BaseState
from gale.input_handler import InputData
from gale.text import render_text
from typing import TypeVar
from src.powerups import Cannons
from src.powerups import Projectile
from src.powerups import CannonsPower

import settings
import src.powerups


class PlayState(BaseState):
    def enter(self, **params: dict):
        self.level = params["level"]
        self.score = params["score"]
        self.lives = params["lives"]
        self.paddle = params["paddle"]
        self.balls = params["balls"]
        self.brickset = params["brickset"]
        self.live_factor = params["live_factor"]
        self.points_to_next_live = params["points_to_next_live"]
        self.points_to_next_grow_up = (
            self.score
            + settings.PADDLE_GROW_UP_POINTS * (self.paddle.size + 1) * self.level
        )
        self.powerups = params.get("powerups", [])
        self.cannons = []
        self.projectiles = []
        self.effect_cannon_time = 5
        self.bullets = []


        if not params.get("resume", False):
            self.balls[0].vx = random.randint(-80, 80)
            self.balls[0].vy = random.randint(-170, -100)
            settings.SOUNDS["paddle_hit"].play()

        self.powerups_abstract_factory = AbstractFactory("src.powerups")
        self.border_bounce = True

    def update(self, dt: float) -> None:
        paddlePreviousX = self.paddle.x
        self.paddle.update(dt)
        for ball in self.balls:
            ballSticked = ball in self.paddle.stickedBalls
            if not ballSticked:
                ball.update(dt)
                if self.border_bounce:
                    ball.solve_world_boundaries()
            else: 
                ball.x += self.paddle.x - paddlePreviousX

            # Check collision with the paddle
            if ball.collides(self.paddle):
                if not ballSticked:
                    settings.SOUNDS["paddle_hit"].stop()
                    settings.SOUNDS["paddle_hit"].play()
                    if self.paddle.sticky:
                        ball.y = self.paddle.y - 8
                        self.paddle.stickedBalls.append(ball)
                    else:
                        ball.rebound(self.paddle)
                        ball.push(self.paddle)

            # Check collision with brickset
            if not ball.collides(self.brickset):
                continue

            brick = self.brickset.get_colliding_brick(ball.get_collision_rect())

            if brick is None:
                continue

            brick.hit()
            self.score += brick.score()
            ball.rebound(brick)

            # Check earn life
            if self.score >= self.points_to_next_live:
                settings.SOUNDS["life"].play()
                self.lives = min(3, self.lives + 1)
                self.live_factor += 0.5
                self.points_to_next_live += settings.LIVE_POINTS_BASE * self.live_factor

            # Check growing up of the paddle
            if self.score >= self.points_to_next_grow_up:
                settings.SOUNDS["grow_up"].play()
                self.points_to_next_grow_up += (
                    settings.PADDLE_GROW_UP_POINTS * (self.paddle.size + 1) * self.level
                )
                self.paddle.inc_size()

            # Chance to generate two more balls
            if random.random() < 0.1:
                r = brick.get_collision_rect()
                self.powerups.append(
                    self.powerups_abstract_factory.get_factory("TwoMoreBall").create(
                        r.centerx - random.randint(0, 8), r.centery - 8
                    )
                )
            
            # Chance to generate sticky paddle
            if random.random() < 0.1:
                r = brick.get_collision_rect()
                self.powerups.append(
                    self.powerups_abstract_factory.get_factory("StickyPaddle").create(
                        r.centerx - random.randint(0, 8), r.centery - 8
                    )
                )

            # Chance to generate teleport edges
            if random.random() < 0.6:
                r = brick.get_collision_rect()
                self.powerups.append(
                    self.powerups_abstract_factory.get_factory("TeleportEdges").create(
                        r.centerx - random.randint(0, 8), r.centery - 8
                    )
                )
                
            # Chance to generate cannnons
            if random.random() < 0.1:
               r = brick.get_collision_rect()
               self.powerups.append(
                   self.powerups_abstract_factory.get_factory("CannonsPower").create(
                       r.centerx - random.randint(0, 8), r.centery -8 
                   )
               ) 

        # Removing all balls that are not in play
        self.balls = [ball for ball in self.balls if ball.active]

        self.brickset.update(dt)

        if not self.balls:
            self.lives -= 1
            if self.lives == 0:
                self.state_machine.change("game_over", score=self.score)
            else:
                self.paddle.dec_size()
                self.state_machine.change(
                    "serve",
                    level=self.level,
                    score=self.score,
                    lives=self.lives,
                    paddle=self.paddle,
                    brickset=self.brickset,
                    points_to_next_live=self.points_to_next_live,
                    live_factor=self.live_factor,
                )

        # Update powerups
        for powerup in self.powerups:
            powerup.update(dt)

            if powerup.collides(self.paddle):
                powerup.take(self)

        # Remove powerups that are not in play
        self.powerups = [p for p in self.powerups if p.active]

        # Check victory
        if self.brickset.size == 1 and next(
            (True for _, b in self.brickset.bricks.items() if b.broken), False
        ):
            self.paddle.sticky = False
            self.state_machine.change(
                "victory",
                lives=self.lives,
                level=self.level,
                score=self.score,
                paddle=self.paddle,
                balls=self.balls,
                points_to_next_live=self.points_to_next_live,
                live_factor=self.live_factor,
            )

        if len(self.cannons) > 0:
            self.cannons[0].x = self.paddle.x - self.cannons[0].width
            self.cannons[0].y = self.paddle.y + self.paddle.height // 2 - self.cannons[0].height // 2

            self.cannons[1].x = self.paddle.x + self.paddle.width
            self.cannons[1].y = self.paddle.y + self.paddle.height // 2 - self.cannons[1].height // 2
        
        for projectile in self.projectiles:
            projectile.update(dt)

            if projectile.collides(self.brickset):
                projectile.solve_world_boundaries()

                brick = self.brickset.get_colliding_brick(
                    projectile.get_collision_rect())

                if brick is None:
                    continue

                brick.hit()
                self.score += brick.score()
                projectile.in_play = False
        
        # Actualizar balas
        for bullet in self.bullets:
                bullet.update(dt, self.brickset)
        self.bullets = [b for b in self.bullets if b.active]

    def render(self, surface: pygame.Surface) -> None:
        heart_x = settings.VIRTUAL_WIDTH - 120

        i = 0
        # Draw filled hearts
        while i < self.lives:
            surface.blit(
                settings.TEXTURES["hearts"], (heart_x, 5), settings.FRAMES["hearts"][0]
            )
            heart_x += 11
            i += 1

        # Draw empty hearts
        while i < 3:
            surface.blit(
                settings.TEXTURES["hearts"], (heart_x, 5), settings.FRAMES["hearts"][1]
            )
            heart_x += 11
            i += 1

        render_text(
            surface,
            f"Score: {self.score}",
            settings.FONTS["tiny"],
            settings.VIRTUAL_WIDTH - 80,
            5,
            (255, 255, 255),
        )

        self.brickset.render(surface)

        self.paddle.render(surface)

        for cannon in self.cannons:
            cannon.render(surface)

        for projectile in self.projectiles:
            projectile.render(surface)

        for ball in self.balls:
            ball.render(surface)

        for powerup in self.powerups:
            powerup.render(surface)
            
        # Dibujar balas
        for bullet in self.bullets:
            bullet.render(surface)

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "move_left":
            if input_data.pressed:
                self.paddle.vx = -settings.PADDLE_SPEED
            elif input_data.released and self.paddle.vx < 0:
                self.paddle.vx = 0
        elif input_id == "move_right":
            if input_data.pressed:
                self.paddle.vx = settings.PADDLE_SPEED
            elif input_data.released and self.paddle.vx > 0:
                self.paddle.vx = 0
        elif input_id == "pause" and input_data.pressed:
            self.state_machine.change(
                "pause",
                level=self.level,
                score=self.score,
                lives=self.lives,
                paddle=self.paddle,
                balls=self.balls,
                brickset=self.brickset,
                points_to_next_live=self.points_to_next_live,
                live_factor=self.live_factor,
                powerups=self.powerups,
            )
        elif input_id == "release_ball" and input_data.pressed:
            self.paddle.sticky = False
            self.paddle.stickedBalls.clear()
        # elif input_id == "shoot" and input_data.pressed:
        #     for cannon in self.cannons:
        #         cannon.shoot_projectiles()
        elif input_id == "shoot" and input_data.pressed:
            for powerup in self.powerups:
                if isinstance(powerup, CannonsPower) and powerup.active:
                    powerup._shoot_bullets()
            
            settings.SOUNDS["paddle_hit"].play()
            
    def fill_cannons(self):
        if len(self.cannons) == 0:
            self.cannons.append(
                Cannons(self.paddle.x, self.paddle.y+self.paddle.height, self))
            self.cannons.append(
                Cannons(self.paddle.x-self.paddle.width, self.paddle.y+self.paddle.height, self))      
            
