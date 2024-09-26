import pygame
from random import randint, uniform
from utils import WINDOW_HEIGHT

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, pos, groups, display_surface):
        super().__init__(groups)
        self.display_surface = display_surface
        original_image = pygame.image.load('assets\\graphics\\asteroid.png').convert_alpha()
        asteroid_surf = pygame.transform.scale(original_image, (128, 128))
        asteroid_size = pygame.math.Vector2(asteroid_surf.get_size()) * uniform(0.5, 1.5)
        self.scaled_surf = pygame.transform.scale(asteroid_surf, asteroid_size)
        self.image = self.scaled_surf
        self.rect = self.image.get_rect(center=pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = randint(300, 400)
        self.rotation = 0
        self.rotation_speed = randint(20, 50)

    def rotate(self, dt):
        self.rotation += self.rotation_speed * dt
        rotated_surf = pygame.transform.rotozoom(self.scaled_surf, self.rotation, 1)
        self.image = rotated_surf
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.pos += self.direction * self.speed * dt
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))
        self.rotate(dt)
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()
