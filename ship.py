import pygame
from laser import Laser
import sys
from utils import WINDOW_WIDTH, WINDOW_HEIGHT

class Ship(pygame.sprite.Sprite):
    def __init__(self, groups, laser_group, asteroid_group, display_surface, score):
        super().__init__(groups)
        self.laser_group = laser_group
        self.asteroid_group = asteroid_group
        self.display_surface = display_surface
        self.score = score
        original_image = pygame.image.load('assets\\graphics\\Battleplane.png').convert_alpha()
        self.image = pygame.transform.scale(original_image, (128, 128))
        self.rect = self.image.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
        self.mask = pygame.mask.from_surface(self.image)
        self.can_shoot = True
        self.shoot_time = None
        self.laser_sound = pygame.mixer.Sound('assets\\sound\\laser.wav')

    def input_position(self):
        pos = pygame.mouse.get_pos()
        self.rect.center = pos

    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time > 300:
                self.can_shoot = True

    def laser_shoot(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()
            Laser(self.laser_group, self.rect.midtop, self.asteroid_group, self.score)
            self.laser_sound.play()

    def asteroid_collision(self):
        if pygame.sprite.spritecollide(self, self.asteroid_group, True, pygame.sprite.collide_mask):
            pygame.quit()
            sys.exit()

    def update(self, dt):
        self.laser_timer()
        self.input_position()
        self.laser_shoot()
        self.asteroid_collision()
