import pygame
import sys
from random import randint
from ship import Ship
from laser import Laser
from asteroid import Asteroid
from alien import Alien
from score import Score
from utils import WINDOW_WIDTH, WINDOW_HEIGHT

def restart_game():
    """Restart the game by reinitializing all necessary components."""
    global spaceship_group, laser_group, asteroid_group, alien_group, score, ship, alien
    spaceship_group = pygame.sprite.Group()
    laser_group = pygame.sprite.Group()
    asteroid_group = pygame.sprite.Group()
    alien_group = pygame.sprite.Group()  

    score = Score(display_surface)
    ship = Ship(spaceship_group, laser_group, asteroid_group, display_surface, score)
    alien = None  

def display_intro():
    """Display the introductory screen with game instructions."""
    font = pygame.font.Font('assets\\graphics\\subatomic.ttf', 50)
    title_text = font.render('Asteroid Shooter', True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 100))
    display_surface.blit(title_text, title_rect)

    instructions_font = pygame.font.Font('assets\\graphics\\subatomic.ttf', 30)
    instructions_text1 = instructions_font.render('To control the ship, use the mouse.', True, (255, 255, 255))
    instructions_rect1 = instructions_text1.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 20))
    display_surface.blit(instructions_text1, instructions_rect1)

    instructions_text2 = instructions_font.render('To shoot, use the left mouse click.', True, (255, 255, 255))
    instructions_rect2 = instructions_text2.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 20))
    display_surface.blit(instructions_text2, instructions_rect2)

    start_text = instructions_font.render('To start the game, press SPACE.', True, (255, 255, 255))
    start_rect = start_text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 60))
    display_surface.blit(start_text, start_rect)

    pygame.display.update()

def display_game_over(win=False, score=0):
    """Display 'Game Over' message on the screen."""
    font = pygame.font.Font('assets\\graphics\\subatomic.ttf', 50)
    game_over_text = font.render('Game Over', True, (255, 255, 0))
    game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 100))
    display_surface.blit(game_over_text, game_over_rect)

    if win:
        result_text = font.render('You Win', True, (0, 255, 0))
    else:
        result_text = font.render('You Lose', True, (255, 0, 0))
    result_rect = result_text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 40))
    display_surface.blit(result_text, result_rect)

    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 20))
    display_surface.blit(score_text, score_rect)

    restart_text = font.render('Press SPACE to Restart', True, (255, 255, 255))
    restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 80))
    display_surface.blit(restart_text, restart_rect)

    quit_text = font.render('Press ESC to Quit', True, (255, 255, 255))
    quit_rect = quit_text.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 140))
    display_surface.blit(quit_text, quit_rect)

    pygame.display.update()

# Basic setup
pygame.init()
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Asteroid Shooter')
clock = pygame.time.Clock()
background_surface = pygame.image.load('assets\\graphics\\background.jpg').convert()

# Display intro screen
display_intro()
waiting_for_start = True
while waiting_for_start:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                waiting_for_start = False

# Initialize game components
restart_game()

# Asteroid timer
asteroid_timer = pygame.event.custom_type()
pygame.time.set_timer(asteroid_timer, 500)

# Background music
bg_music = pygame.mixer.Sound('assets\\sound\\spacemusic.wav')
bg_music.play(loops=-1)

# Game loop
game_over = False
win = False
FPS = 60  # Set FPS
while True:
    dt = clock.tick(FPS) / 1000  # Ensure the game runs at 60 FPS

    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == asteroid_timer and not ship.destroyed:
            asteroid_y_pos = randint(-150, -50)
            asteroid_x_pos = randint(-100, WINDOW_WIDTH + 100)
            Asteroid((asteroid_x_pos, asteroid_y_pos), asteroid_group, display_surface, score)
        if event.type == pygame.KEYDOWN:
            if game_over:
                if event.key == pygame.K_SPACE:
                    restart_game()
                    game_over = False
                    win = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    # Background
    display_surface.blit(background_surface, (0, 0))

    if ship.destroyed:
        spaceship_group.draw(display_surface)  # Draw the destroyed ship
        display_game_over(win=False, score=score.score)
        game_over = True
        continue

    if alien and alien.destroyed:
        alien_group.draw(display_surface)  # Draw the destroyed alien ship
        display_game_over(win=True, score=score.score)
        game_over = True
        continue

    # Check if score is greater than 50 to spawn alien
    if score.score > 50 and alien is None:
        alien = Alien(alien_group, laser_group, display_surface, score)

    # Update
    spaceship_group.update(dt)
    laser_group.update(dt)
    asteroid_group.update(dt)
    if alien:
        alien_group.update(dt)

    score.display()

    # Graphics
    spaceship_group.draw(display_surface)
    laser_group.draw(display_surface)
    asteroid_group.draw(display_surface)
    if alien:
        alien_group.draw(display_surface)

    # Draw the frame
    pygame.display.update()
