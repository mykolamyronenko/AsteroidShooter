import pygame
from laser import Laser
import sys
from utils import WINDOW_WIDTH, WINDOW_HEIGHT

class Ship(pygame.sprite.Sprite):
    def __init__(self, groups, laser_group, asteroid_group, display_surface, score):
        """Initialize the ship with its groups, laser group, asteroid group, display surface, and score."""
        super().__init__(groups)
        self.laser_group = laser_group
        self.asteroid_group = asteroid_group
        self.display_surface = display_surface
        self.score = score
        
        # Load and scale the ship image
        original_image = pygame.image.load('assets\\graphics\\Battleplane.png').convert_alpha()
        self.image = pygame.transform.scale(original_image, (128, 128))
        self.original_image = self.image.copy()
        
        # Set initial position and mask
        self.rect = self.image.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.mask = pygame.mask.from_surface(self.image)
        
        # Shooting attributes
        self.can_shoot = True
        self.shoot_time = None
        self.laser_sound = pygame.mixer.Sound('assets\\sound\\laser.wav')
        
        # Explosion and hit attributes
        self.explosion_sound = pygame.mixer.Sound('assets\\sound\\explosion.wav')
        self.laser_hit_sound = pygame.mixer.Sound('assets\\sound\\laserhit.wav')
        self.destroyed_image = pygame.image.load('assets\\graphics\\destroyed.png').convert_alpha()
        self.destroyed = False
        self.hit_count = 0
        self.max_hits = 3
        self.hit_time = None

    def input_position(self):
        """Update the ship's position based on the mouse position."""
        pos = pygame.mouse.get_pos()
        self.rect.center = pos

    def laser_timer(self):
        """Manage the shooting cooldown for the ship."""
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time > 300:  # 300 ms cooldown
                self.can_shoot = True

    def laser_shoot(self):
        """Shoot a laser if the ship can shoot."""
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()
            Laser(self.laser_group, self.rect.midtop, self.asteroid_group, self.score)
            self.laser_sound.play()

    def asteroid_collision(self):
        """Check for collisions with asteroids and handle the collision."""
        if pygame.sprite.spritecollide(self, self.asteroid_group, True, pygame.sprite.collide_mask):
            self.image = self.destroyed_image
            self.explosion_sound.play()
            self.destroyed = True

    def laser_collision(self):
        """Check for collisions with alien lasers and handle the collision."""
        for laser in self.laser_group:
            if laser.is_alien and pygame.sprite.collide_mask(self, laser):
                laser.kill()
                self.hit_count += 1
                self.hit_time = pygame.time.get_ticks()
                self.image.fill((255, 0, 0), special_flags=pygame.BLEND_MULT)
                self.laser_hit_sound.play()
                if self.hit_count >= self.max_hits:
                    self.image = self.destroyed_image
                    self.explosion_sound.play()
                    self.destroyed = True

    def update(self, dt):
        """Update the ship's position, shooting, and collision detection."""
        if not self.destroyed:
            self.laser_timer()
            self.input_position()
            self.laser_shoot()
            self.asteroid_collision()
            self.laser_collision()
            if self.hit_time and pygame.time.get_ticks() - self.hit_time > 100:
                self.image = self.original_image.copy()
