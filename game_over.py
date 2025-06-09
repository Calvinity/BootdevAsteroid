import pygame
from constants import *

class GameOver:
    def __init__(self):
        self.font = pygame.font.SysFont("Arial", 36)
        self.game_over_font = pygame.font.SysFont("Arial", 72)
        self.show_easter_egg = False
        self.easter_egg_sequence = []
    
    def handle_event(self, event):
        """Handle keyboard events for game over screen"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and not self.show_easter_egg:
                return "restart"
            elif event.key == pygame.K_q:
                return "quit"
            elif event.key == pygame.K_ESCAPE and self.show_easter_egg:
                self.show_easter_egg = False
                return None
            elif not self.show_easter_egg:
                # Easter egg sequence tracking
                if event.key == pygame.K_e and len(self.easter_egg_sequence) == 0:
                    self.easter_egg_sequence = ['e']
                elif event.key == pygame.K_l and self.easter_egg_sequence == ['e']:
                    self.easter_egg_sequence = ['e', 'l']
                elif event.key == pygame.K_l and self.easter_egg_sequence == ['e', 'l']:
                    self.easter_egg_sequence = ['e', 'l', 'l']
                elif event.key == pygame.K_i and self.easter_egg_sequence == ['e', 'l', 'l']:
                    self.easter_egg_sequence = ['e', 'l', 'l', 'i']
                elif event.key == pygame.K_e and self.easter_egg_sequence == ['e', 'l', 'l', 'i']:
                    self.show_easter_egg = True
                    self.easter_egg_sequence = []
                else:
                    self.easter_egg_sequence = []  # Reset on wrong key

            elif event.key == pygame.K_ESCAPE and self.show_easter_egg:
                self.show_easter_egg = False  # Hide easter egg and return to normal game over

    def draw(self, screen, score):
        """Draw the game over screen"""
        screen.fill("black")
        
        if self.show_easter_egg:
            # Easter egg display
            easter_egg_text = self.game_over_font.render("Ellie är bäst!", True, (255, 255, 255))
            easter_egg_rect = easter_egg_text.get_rect()
            easter_egg_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
            screen.blit(easter_egg_text, easter_egg_rect)
            
            # Instructions to go back
            back_text = self.font.render("Press ESC to go back", True, (255, 165, 0))
            back_rect = back_text.get_rect()
            back_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)
            screen.blit(back_text, back_rect)
            
        else:
            # Normal game over screen
            game_over_text = self.game_over_font.render("GAME OVER!", True, (255, 255, 255))
            game_over_rect = game_over_text.get_rect()
            game_over_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
            screen.blit(game_over_text, game_over_rect)
            
            # Score text below it
            score_text = self.font.render(f"Final Score: {score}", True, (255, 165, 0))
            score_rect = score_text.get_rect()
            score_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30)
            screen.blit(score_text, score_rect)

        # Restart instruction - ALWAYS SHOWN
        restart_text = self.font.render("Press R to Restart or Q to Quit", True, (255, 255, 255))
        restart_rect = restart_text.get_rect()
        restart_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80)
        screen.blit(restart_text, restart_rect)