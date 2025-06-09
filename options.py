import pygame
from constants import *
from menu import MenuButton

class Options:
    def __init__(self):
        self.font = pygame.font.Font(None, 48)
        self.master_volume = 0.7
        self.should_go_back = False
        
        # Volume control buttons
        self.volume_up_button = MenuButton(
            SCREEN_WIDTH//2 + 100, 300, 60, 40,
            "+", self.font, self.volume_up
        )
        
        self.volume_down_button = MenuButton(
            SCREEN_WIDTH//2 - 160, 300, 60, 40,
            "-", self.font, self.volume_down
        )
        
        self.back_button = MenuButton(
            SCREEN_WIDTH//2 - 100, 400, 200, 60,
            "BACK TO MENU", self.font, self.back_to_menu
        )
        
        self.buttons = [self.volume_up_button, self.volume_down_button, self.back_button]

    def update_cooldown(self, dt):
        """Call this every frame to update the cooldown timer"""
        if self.volume_cooldown > 0:
            self.volume_cooldown -= dt
    
    def volume_up(self):
        if self.volume_cooldown <= 0:  # Only change if cooldown is finished
            self.master_volume = min(1.0, self.master_volume + 0.1)
            self.volume_cooldown = 0.2  # 200ms cooldown between changes
        return "volume_up"
    
    def volume_down(self):
        if self.volume_cooldown <= 0:  # Only change if cooldown is finished
            self.master_volume = max(0.0, self.master_volume - 0.1)
            self.volume_cooldown = 0.2  # 200ms cooldown between changes
        return "volume_down"
    
    def back_to_menu(self):
        self.should_go_back = True
        return "back_to_menu"