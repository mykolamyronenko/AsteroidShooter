import pygame
from laser import Laser
from utils import WINDOW_WIDTH

class Alien(pygame.sprite.Sprite):
    def __init__(self, groups, laser_group, display_surface, score):
        """Initialize the alien with its groups, laser group, display surface, and score."""
        super().__init__(groups)
        self.laser_group = laser_group
        self.display_surface = display_surface
        self.score = score
        
        # Load and scale the alien image
        origin_image = pygame.image.load('assets\\graphics\\alien.png').convert_alpha()
        self.image = pygame.transform.scale(origin_image, (128, 128))
        self.original_image = self.image.copy()
        
        # Load the destroyed image
        self.destroyed_image = pygame.image.load('assets\\graphics\\destroyed.png').convert_alpha()
        
        # Set initial position and mask
        self.rect = self.image.get_rect(midtop=(WINDOW_WIDTH / 2, 50))
        self.mask = pygame.mask.from_surface(self.image)
        
        # Set movement and shooting attributes
        self.direction = 1  # 1 for right, -1 for left
        self.speed = 300  
        self.can_shoot = True
        self.shoot_time = None
        
        # Load sounds
        self.laser_sound = pygame.mixer.Sound('assets\\sound\\alien_laser.wav')
        self.laser_hit_sound = pygame.mixer.Sound('assets\\sound\\laserhit.wav')
        
        # Set hit attributes
        self.hit_count = 0
        self.max_hits = 5
        self.hit_time = None
        self.destroyed = False

    def move(self, dt):
        """Move the alien horizontally and change direction at screen edges."""
        self.rect.x += self.direction * self.speed * dt
        if self.rect.right >= WINDOW_WIDTH or self.rect.left <= 0:
            self.direction *= -1

    def laser_timer(self):
        """Manage the shooting cooldown for the alien."""
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shoot_time > 500:  # Alien shoots every 0.5 seconds
                self.can_shoot = True

    def laser_shoot(self):
        """Shoot a laser if the alien can shoot."""
        if self.can_shoot:
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()
            Laser(self.laser_group, self.rect.midbottom, None, self.score, is_alien=True)  # No target, shoots straight down
            self.laser_sound.play()

    def check_hits(self):
        """Check if the alien has been hit enough times to be destroyed."""
        if self.hit_count >= self.max_hits:
            self.image = self.destroyed_image
            self.destroyed = True
            self.score.increment(20)  # Increase score by 20 points

    def laser_collision(self):
        """Check for collisions with player lasers and handle the collision."""
        for laser in self.laser_group:
            if not laser.is_alien and pygame.sprite.collide_mask(self, laser):
                laser.kill()
                self.hit_count += 1
                self.hit_time = pygame.time.get_ticks()
                self.image.fill((255, 0, 0), special_flags=pygame.BLEND_MULT)
                self.laser_hit_sound.play()
                self.check_hits()

    def update(self, dt):
        """Update the alien's position, shooting, and collision detection."""
        if not self.destroyed:
            self.move(dt)
            self.laser_timer()
            self.laser_shoot()
            self.laser_collision()
            if self.hit_time and pygame.time.get_ticks() - self.hit_time > 100:
                self.image = self.original_image.copy()
