from circleshape import CircleShape
from constants import *
import pygame
from shot import *
from weapon import *


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.weapon = Weapon("basic")
        self.shot_cd = 0

    # in the player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        pygame.draw.polygon(screen, "blue", self.triangle(), 2)

        
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt
        

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
        if self.shot_cd > 0:
            self.shot_cd -= dt

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

        # Screen wrapping
        if self.position.x < 0:
            self.position.x = SCREEN_WIDTH
        elif self.position.x > SCREEN_WIDTH:
            self.position.x = 0
            
        if self.position.y < 0:
            self.position.y = SCREEN_HEIGHT
        elif self.position.y > SCREEN_HEIGHT:
            self.position.y = 0

    def shoot(self):
        if self.shot_cd > 0:
            return  # Still cooling down, don't shoot
        
        # Fire the weapon and reset cooldown
        shots = self.weapon.fire(self.position, self.rotation)
        self.shot_cd = PLAYER_SHOOT_COOLDOWN  # Reset the timer
        return shots

    def upgrade_weapon(self, score):
        if score >= 300:
            self.weapon = Weapon("triple")
        elif score >= 600:
            self.weapon = Weapon("spread")










