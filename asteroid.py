from circleshape import CircleShape
import pygame
from constants import *
import random


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "red", (int(self.position.x), int(self.position.y)), self.radius, 2)


    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        ricochet_angle = random.uniform(20, 50)
        velocity1 =self.velocity.rotate(ricochet_angle)
        velocity2 = self.velocity.rotate(-ricochet_angle)
        new_asteroid1 = Asteroid(self.position.x, self.position.y, self.radius / 2)
        new_asteroid1.velocity = velocity1 * 1.2
        new_asteroid2 = Asteroid(self.position.x, self.position.y, self.radius / 2)
        new_asteroid2.velocity = velocity2 * 1.2



























