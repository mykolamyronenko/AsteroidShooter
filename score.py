import pygame
from utils import WINDOW_WIDTH, WINDOW_HEIGHT

class Score:
    def __init__(self, display_surface):
        self.display_surface = display_surface
        self.font = pygame.font.Font('assets\\graphics\\subatomic.ttf', 50)
        self.score = 0

    def increment(self):
        self.score += 1

    def display(self):
        score_text = f'Score: {self.score}'
        text_surface = self.font.render(score_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(midbottom=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 80))
        self.display_surface.blit(text_surface, text_rect)
        pygame.draw.rect(
            self.display_surface,
            (255, 255, 255),
            text_rect.inflate(30, 30),
            width=8,
            border_radius=5
        )
