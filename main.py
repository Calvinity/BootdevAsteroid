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


def draw_score(screen, score, font):
    score_text = font.render(f"Score: {score}", True, (255, 165, 0))
    text_rect = score_text.get_rect()
    text_rect.centerx = SCREEN_WIDTH // 2
    text_rect.y = 10
    screen.blit(score_text, text_rect)


def main():
    pygame.init()
    audio_enabled = False
    shoot_sound = None
    explosion_sound = None
    background_music = None
    easter_egg_sequence = []
    show_easter_egg = False
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
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    game_over_font = pygame.font.SysFont("Arial", 72)
    asteroid_field = AsteroidField()
    game_over = False
    while True:
        if not game_over:
            keys = pygame.key.get_pressed()
            screen.fill("black")
            for sprite in drawable:
                sprite.draw(screen)
            updatable.update(dt)
            for asteroid in asteroids:
                if asteroid.collides_with(player):
                    print("Game over!")
                    game_over = True
            for asteroid in asteroids:
                for shot in shots:
                    if asteroid.collides_with(shot):
                        asteroid.split()
                        shot.kill()
                        if audio_enabled and explosion_sound:
                            explosion_sound.play()
                        score += 10
                        player.upgrade_weapon(score)
            draw_score(screen, score, font)

            if keys[pygame.K_SPACE]:
                player.shoot()
                if audio_enabled and shoot_sound:
                    shoot_sound.play()
            


        else:
        # Game over screen   
            screen.fill("black")
        
            if show_easter_egg:
                # Easter egg display
                easter_egg_text = game_over_font.render("Ellie är bäst!", True, (255, 255, 255))
                easter_egg_rect = easter_egg_text.get_rect()
                easter_egg_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
                screen.blit(easter_egg_text, easter_egg_rect)
                
                # Instructions to go back
                back_text = font.render("Press ESC to go back", True, (255, 165, 0))
                back_rect = back_text.get_rect()
                back_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)
                screen.blit(back_text, back_rect)
                
            else:
                # Normal game over screen
                # Game over text
                game_over_text = game_over_font.render("GAME OVER!", True, (255, 255, 255))
                game_over_rect = game_over_text.get_rect()
                game_over_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
                screen.blit(game_over_text, game_over_rect)
                
                # Score text below it
                score_text = font.render(f"Final Score: {score}", True, (255, 165, 0))
                score_rect = score_text.get_rect()
                score_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30)
                screen.blit(score_text, score_rect)

            # Restart instruction - ALWAYS SHOWN (moved outside the if/else blocks)
            restart_text = font.render("Press R to Restart or Q to Quit", True, (255, 255, 255))
            restart_rect = restart_text.get_rect()
            restart_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80)
            screen.blit(restart_text, restart_rect)
            
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_r and not show_easter_egg:
                    # Restart the game - reset all variables
                    game_over = False
                    score = 0
                    shot_timer = 0
                    show_easter_egg = False  # Reset easter egg
                    easter_egg_sequence = []  # Reset sequence
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
                    
                elif event.key == pygame.K_q:
                    return  # Quit the game
                # Easter egg sequence tracking
                elif not show_easter_egg:  # Only track if easter egg isn't showing
                    if event.key == pygame.K_e and len(easter_egg_sequence) == 0:
                        easter_egg_sequence = ['e']
                    elif event.key == pygame.K_l and easter_egg_sequence == ['e']:
                        easter_egg_sequence = ['e', 'l']
                    elif event.key == pygame.K_l and easter_egg_sequence == ['e', 'l']:
                        easter_egg_sequence = ['e', 'l', 'l']
                    elif event.key == pygame.K_i and easter_egg_sequence == ['e', 'l', 'l']:
                        easter_egg_sequence = ['e', 'l', 'l', 'i']
                    elif event.key == pygame.K_e and easter_egg_sequence == ['e', 'l', 'l', 'i']:
                        show_easter_egg = True
                        easter_egg_sequence = []
                    else:
                        easter_egg_sequence = []  # Reset on wrong key

                elif event.key == pygame.K_ESCAPE and show_easter_egg:
                    show_easter_egg = False  # Hide easter egg and return to normal game over




        delta_time_ms = clock.tick(60)
        dt = delta_time_ms / 1000.0















if __name__ == "__main__":
    main()