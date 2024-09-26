import pygame

class Laser(pygame.sprite.Sprite):
    def __init__(self, groups, pos, asteroid_group, score):
        super().__init__(groups)
        self.asteroid_group = asteroid_group
        self.score = score
        self.image = pygame.image.load('assets\\graphics\\laser.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(0, -1)
        self.speed = 800  
        self.explosion_sound = pygame.mixer.Sound('assets\\sound\\explosion.wav')

    def asteroid_collision(self):
        if pygame.sprite.spritecollide(self, self.asteroid_group, True, pygame.sprite.collide_mask):
            self.kill()
            self.explosion_sound.play()
            self.score.increment()

    def update(self, dt):
        self.pos += self.direction * self.speed * dt 
        self.rect.topleft = (round(self.pos.x), round(self.pos.y))
        if self.rect.bottom < 0:
            self.kill()
        self.asteroid_collision()
