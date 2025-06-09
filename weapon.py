import pygame
from constants import *
from shot import Shot

class Weapon:
    def __init__(self, weapon_type="basic"):
        self.weapon_type = weapon_type
        # Define cooldowns for each weapon type
        self.cooldowns = {
            "basic": PLAYER_SHOOT_COOLDOWN,
            "triple": PLAYER_SHOOT_COOLDOWN,
            "burst": 0.15  # Faster firing for burst weapon
        }
    
    def fire(self, player_pos, player_rotation):
        if self.weapon_type == "basic":
            shots = self._fire_single(player_pos, player_rotation)
        elif self.weapon_type == "triple":
            shots = self._fire_triple(player_pos, player_rotation)
        elif self.weapon_type == "burst":
            shots = self._fire_triple(player_pos, player_rotation)
        
        # Return both shots and the cooldown for this weapon
        return shots, self.cooldowns[self.weapon_type]
    
    def _fire_single(self, pos, rotation):
        shot = Shot(pos.x, pos.y, SHOT_RADIUS)
        shot.velocity = pygame.Vector2(0, 1).rotate(rotation) * PLAYER_SHOT_SPEED
        return [shot]
    
    def _fire_triple(self, pos, rotation):
        shots = []
        for angle_offset in [-20, 0, 20]:
            shot = Shot(pos.x, pos.y, SHOT_RADIUS)
            direction = pygame.Vector2(0, 1).rotate(rotation + angle_offset)
            shot.velocity = direction * PLAYER_SHOT_SPEED
            shots.append(shot)
        return shots
    

