import pygame
from constants import *

class MenuButton:
    def __init__(self, x, y, width, height, text, font, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.action = action
        self.hovered = False
        self.clicked = False
    
    def update(self, mouse_pos, mouse_clicked):
        self.hovered = self.rect.collidepoint(mouse_pos)
        if self.hovered and mouse_clicked:
            self.clicked = True
            if self.action:
                return self.action()  # Return action result
        else:
            self.clicked = False
        return None
    
    def draw(self, screen):
        # Color based on state
        if self.clicked:
            color = (100, 100, 100)
        elif self.hovered:
            color = (150, 150, 150)
        else:
            color = (80, 80, 80)
        
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
        
        # Centered text
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

class Menu:
    def __init__(self):
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 36)
        self.master_volume = 0.7
        self.sfx_volume = 0.7
        self.music_volume = 0.7
        self.should_start = False
        self.should_quit = False
        self.should_show_options = False
        self.in_options = False
        self.volume_cooldown = 0.0

        # Create buttons
        self.start_button = MenuButton(
            SCREEN_WIDTH//2 - 100, 200, 250, 60,
            "START GAME", self.font, self.start_game
        )
        
        self.options_button = MenuButton(
            SCREEN_WIDTH//2 - 100, 300, 250, 60,
            "OPTIONS", self.font, self.options
        )
        
        
        self.quit_button = MenuButton(
            SCREEN_WIDTH//2 - 100, 450, 250, 60,
            "QUIT", self.font, self.quit_game
        )

        self.volume_up_button = MenuButton(
            SCREEN_WIDTH//2 + 50, 250, 60, 40,
            "+", self.font, self.volume_up
        )
        
        self.volume_down_button = MenuButton(
            SCREEN_WIDTH//2 - 110, 250, 60, 40,
            "-", self.font, self.volume_down
        )
        
        self.back_button = MenuButton(
            SCREEN_WIDTH//2 - 100, 350, 200, 60,
            "BACK", self.font, self.back_to_main
        )


        self.main_buttons = [self.start_button, self.options_button, self.quit_button]
        self.options_buttons = [self.volume_up_button, self.volume_down_button, self.back_button]
        self.buttons = self.main_buttons
    
    def start_game(self):
        self.should_start = True
        return "start"
    
    def options(self):
        self.should_show_options = True
        return "options"

    def quit_game(self):
        self.should_quit = True
        return "quit"
    
    def back_to_main(self):
        self.in_options = False
        self.buttons = self.main_buttons  # Switch back to main buttons
        return "back"
    
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
    
    def update_cooldown(self, dt):
        """Call this every frame to update the cooldown timer"""
        if self.volume_cooldown > 0:
            self.volume_cooldown -= dt


    def draw_volume_display(self, screen, font):
        if self.in_options:
            volume_text = font.render(f"Master Volume: {int(self.master_volume * 100)}%", True, "white")
            volume_rect = volume_text.get_rect(center=(SCREEN_WIDTH//2, 200))
            screen.blit(volume_text, volume_rect)



















