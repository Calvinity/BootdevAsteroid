# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame
import sys
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import *
from circleshape import *
from shot import *
import pygame.font
from weapon import *
import os
from menu import *
from mouse import *
from game_state import *
from game_over import GameOver


updatable = pygame.sprite.Group()
drawable = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
shots = pygame.sprite.Group()

Player.containers = (updatable, drawable)
Asteroid.containers = (updatable, drawable, asteroids)
AsteroidField.containers = (updatable,)
Shot.containers = (updatable, drawable, shots)

def get_resource_path(relative_path):
    """Get absolute path to resource, works for both development and PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def draw_ui(screen, score, game_time, difficulty_level, font):
    # Score (centered at top)
    score_text = font.render(f"Score: {score}", True, (255, 165, 0))
    text_rect = score_text.get_rect()
    text_rect.centerx = SCREEN_WIDTH // 2
    text_rect.y = 10
    screen.blit(score_text, text_rect)
    
    # Timer (top left)
    minutes = int(game_time // 60)
    seconds = int(game_time % 60)
    time_text = font.render(f"Time: {minutes:02d}:{seconds:02d}", True, (255, 255, 255))
    screen.blit(time_text, (10, 10))
    
    # Difficulty (top left, below timer)
    displayed_difficulty = difficulty_level + 1
    diff_text = font.render(f"Level: {displayed_difficulty}", True, (255, 100, 100))
    screen.blit(diff_text, (10, 50))


def main():
    pygame.init()
    current_state = GameState.MENU
    audio_enabled = False
    shoot_sound = None
    explosion_sound = None
    background_music = None
    try:
        pygame.mixer.init()
        shoot_sound = pygame.mixer.Sound(get_resource_path("sounds/shoot.wav"))
        explosion_sound = pygame.mixer.Sound(get_resource_path("sounds/explosion.wav"))
        background_music = pygame.mixer.Sound(get_resource_path("sounds/background.wav"))
        audio_enabled = True
        print("Audio loaded successfully!")

        if background_music:
            pygame.mixer.Sound.play(background_music, loops=-1)

    except (pygame.error, FileNotFoundError) as e:
        print(f"Audio disabled: {e}")
        audio_enabled = False
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    score = 0
    font = pygame.font.SysFont("Arial", 36)

    menu = Menu()
    game_over_screen = GameOver()

    player = None
    asteroid_field = None

    while True:
        if current_state == GameState.MENU:
            screen.fill("black")
            menu.update_cooldown(dt)
            
            # Handle menu input every frame
            mouse_pos = pygame.mouse.get_pos()
            mouse_clicked = pygame.mouse.get_pressed()[0]
            
            # Update and draw menu buttons every frame
            for button in menu.buttons:
                button.update(mouse_pos, mouse_clicked)
                button.draw(screen)
            
            # Draw title
            title_font = pygame.font.Font(None, 72)
            title = title_font.render("ASTEROIDS", True, "green")
            title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 100))
            screen.blit(title, title_rect)

            menu.draw_volume_display(screen, font)
            
            # Only transition when button is clicked
            if menu.should_start:
                current_state = GameState.PLAYING
                player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                asteroid_field = AsteroidField()
                score = 0
                menu.should_start = False

            elif menu.should_show_options:
                menu.in_options = True
                menu.buttons = menu.options_buttons  # Switch button set
                menu.should_show_options = False
                

            elif menu.should_quit:
                return

        elif current_state == GameState.PLAYING:
            keys = pygame.key.get_pressed()
            screen.fill("black")
            for sprite in drawable:
                sprite.draw(screen)
            updatable.update(dt)
            for asteroid in asteroids:
                if asteroid.collides_with(player):
                    print("Game over!")
                    current_state = GameState.GAME_OVER
                    break
            if current_state == GameState.PLAYING:
                for asteroid in asteroids:
                    for shot in shots:
                        if asteroid.collides_with(shot):
                            asteroid.split()
                            shot.kill()
                            if audio_enabled and explosion_sound:
                                explosion_sound.set_volume(menu.master_volume)
                                explosion_sound.play()
                            score += 10
                            player.upgrade_weapon(score)

            for sprite in drawable:
                sprite.draw(screen)

            difficulty_level = int(asteroid_field.game_time // asteroid_field.difficulty_interval)
            draw_ui(screen, score, asteroid_field.game_time, difficulty_level, font)

            if keys[pygame.K_SPACE]:
                player.shoot()
                if audio_enabled and shoot_sound:
                    shoot_sound.set_volume(menu.master_volume)
                    shoot_sound.play()
            


        elif current_state == GameState.GAME_OVER:
            game_over_screen.draw(screen, score)
            
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if current_state == GameState.GAME_OVER:
                action = game_over_screen.handle_event(event)
                if action == "restart":
                    current_state = GameState.PLAYING
                    score = 0
                    # Clear all existing sprites
                    for sprite in updatable:
                        sprite.kill()
                    for sprite in drawable:
                        sprite.kill()
                    for sprite in asteroids:
                        sprite.kill()
                    for sprite in shots:
                        sprite.kill()
                    if audio_enabled and background_music:
                        pygame.mixer.stop()
                        pygame.mixer.Sound.play(background_music, loops=-1)
                    # Recreate the player and asteroid field
                    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                    asteroid_field = AsteroidField()
                elif action == "quit":
                    return

                    




        delta_time_ms = clock.tick(60)
        dt = delta_time_ms / 1000.0















if __name__ == "__main__":
    main()