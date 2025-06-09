import pygame

class MenuButton:
    def __init__(self, x, y, width, height, text, font, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.action = action
        self.hovered = False
        self.clicked = False
    
    def update(self, mouse_pos, mouse_clicked):
        # Check if mouse is hovering
        self.hovered = self.rect.collidepoint(mouse_pos)
        
        # Check if button was clicked
        if self.hovered and mouse_clicked:
            self.clicked = True
            if self.action:
                self.action()
        else:
            self.clicked = False
    
    def draw(self, screen):
        # Change color based on state
        if self.clicked:
            color = (100, 100, 100)  # Dark gray when clicked
        elif self.hovered:
            color = (150, 150, 150)  # Light gray when hovered
        else:
            color = (200, 200, 200)  # White normally
        
        # Draw button
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)  # Border
        
        # Draw text centered
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

