import pygame
from Client_side.App.GameObject import GameObject  # Assuming GameObject class is in GameObject.py

class PlusButton(GameObject):
    def __init__(self, x, y, width, height, color=(29, 64, 99),):
        super().__init__(x, y, width, height, color)
        self.button_radius = width // 2  # Half of the width to make it circular
        self.button_center = (x, y)  # Center of the button
        self.font = pygame.font.Font(None, 150)  # Built-in font for the plus sign

    def render(self, screen, camera):
        """Render the circular plus button"""
        # Draw the circle for the button
        pygame.draw.circle(screen, self.color, self.button_center, self.button_radius)

        # Render the plus sign inside the button
        plus_text = self.font.render("+", True, (255, 255, 255))  # White plus sign

        # Position the plus sign at the center of the button, with slight adjustments
        self.plus_rect = plus_text.get_rect(center=self.button_center)
        self.plus_rect.y -= 5  # Shift the plus sign slightly upwards (optional)
        screen.blit(plus_text, self.plus_rect)

    def on_click(self, mouse_pos):
        """Check if the story was clicked."""
        if self.plus_rect.collidepoint(mouse_pos):
            print(f"Add Story clicked at {mouse_pos}")
            return True
        return False