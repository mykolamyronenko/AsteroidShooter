import pygame
from utils import WINDOW_WIDTH, WINDOW_HEIGHT

class Score:
    def __init__(self, display_surface):
        """Initialize the score with the display surface."""
        self.display_surface = display_surface
        self.font = pygame.font.Font('assets\\graphics\\subatomic.ttf', 30)  # Load the font for displaying the score
        self.score = 0  # Initialize the score to zero

    def increment(self, amount=1):
        """Increment the score by a specified amount (default is 1)."""
        self.score += amount

    def display(self):
        """Display the current score on the screen."""
        score_text = f'Score: {self.score}'  # Create the score text
        text_surface = self.font.render(score_text, True, (255, 255, 255))  # Render the score text
        text_rect = text_surface.get_rect(topleft=(20, 20))  # Position the score text at the top-left corner
        self.display_surface.blit(text_surface, text_rect)  # Draw the score text on the display surface
        
        # Draw a rectangle around the score text for better visibility
        pygame.draw.rect(
            self.display_surface,
            (255, 255, 255),
            text_rect.inflate(10, 10),
            width=2,
            border_radius=5
        )
