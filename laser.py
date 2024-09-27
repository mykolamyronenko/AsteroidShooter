import pygame
from utils import WINDOW_HEIGHT

class Laser(pygame.sprite.Sprite):
    def __init__(self, groups, pos, asteroid_group, score, target=None, is_alien=False):
        """Initialize the laser with its position, groups, target, and type (player or alien)."""
        super().__init__(groups)
        self.asteroid_group = asteroid_group
        self.score = score
        self.target = target
        self.is_alien = is_alien
        
        # Load the appropriate laser image based on whether it's an alien laser
        if self.is_alien:
            self.image = pygame.image.load('assets\\graphics\\alien_laser.png').convert_alpha()
            self.direction = pygame.math.Vector2(0, 1)  # Downward for alien lasers
        else:
            self.image = pygame.image.load('assets\\graphics\\laser.png').convert_alpha()
            self.direction = pygame.math.Vector2(0, -1)  # Upward for player lasers
        
        self.rect = self.image.get_rect(midbottom=pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.speed = 800  # Speed of the laser
        
        # Load the explosion sound
        self.explosion_sound = pygame.mixer.Sound('assets\\sound\\explosion.wav')

    def asteroid_collision(self):
        """Check for collisions with asteroids and handle the collision."""
        if self.asteroid_group and pygame.sprite.spritecollide(self, self.asteroid_group, True, pygame.sprite.collide_mask):
            self.kill()
            self.explosion_sound.play()
            self.score.increment()

    def target_collision(self):
        """Check for collisions with the target (e.g., the player's ship) and handle the collision."""
        if self.target and pygame.sprite.spritecollide(self, self.target, False, pygame.sprite.collide_mask):
            self.kill()
            self.target.hit_count += 1
            self.target.hit_time = pygame.time.get_ticks()  # Record the hit time
            self.explosion_sound.play()

    def update(self, dt):
        """Update the laser's position and check for collisions."""
        self.pos += self.direction * self.speed * dt 
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))
        
        # Remove the laser if it moves off the screen
        if self.rect.bottom < 0 or self.rect.top > WINDOW_HEIGHT:
            self.kill()
        
        # Check for collisions
        self.asteroid_collision()
        self.target_collision()
