import pygame
from Client_side.App.GameObject import GameObject  # Assuming GameObject class is in GameObject.py
import math  # To calculate distance for circle hover

class Button(GameObject):
    def __init__(self,button_name,  x, y, width, height, color, hover_color, text, border_radius=None, num_of_side=0, text_size = 24):
        super().__init__(x, y, width, height, color)
        self.button_name= button_name
        self.font = pygame.font.Font("../font.ttf", text_size)
        self.hover_color = hover_color
        self.text = text
        self.is_hovered = False
        self.border_radius = border_radius  # Rounded corners radius
        self.num_of_side = num_of_side

    def render(self, screen, camera = None):
        """Render the rectangular or circular button with dynamic color on hover and rounded corners"""
        # Check for mouse hover
        mouse_pos = pygame.mouse.get_pos()

        # Check if mouse is inside the button's area (rectangle or circle)
        if self.num_of_side == 4:
            self.is_hovered = self.get_rect().collidepoint(mouse_pos)
        elif self.num_of_side == 0:
            # For circle, calculate the distance between the mouse and the center
            distance = math.sqrt((mouse_pos[0] - self.x) ** 2 + (mouse_pos[1] - self.y) ** 2)
            self.is_hovered = distance <= self.border_radius



        # Draw the button with the appropriate color (hover or normal)
        current_color = self.hover_color if self.is_hovered else self.color
        if self.num_of_side == 4:
            pygame.draw.rect(screen, current_color, self.get_rect(), border_radius=self.border_radius)
        elif self.num_of_side == 0:
            # Draw a circle
            pygame.draw.circle(screen, current_color, (self.x, self.y), self.border_radius)

        # Render the text inside the button
        text_surface = self.font.render(self.text, True, (255, 255, 255))  # White text
        text_rect = 0
        if self.num_of_side == 4:
            text_rect = text_surface.get_rect(center=pygame.Rect(self.x, self.y, self.width, self.height).center)
        elif self.num_of_side == 0:
            # Draw a circle
            text_rect = text_surface.get_rect(center=(self.x, self.y))

        screen.blit(text_surface, text_rect)

    def on_click(self, mouse_pos):
        """Check if the button was clicked and mouse is hovered over it."""
        if self.is_hovered:
            # For circle, check if the click is within the circle
            if self.num_of_side == 0:
                distance = math.sqrt((mouse_pos[0] - self.x) ** 2 + (mouse_pos[1] - self.y) ** 2)
                if distance <= self.border_radius:
                    print(f"Button '{self.text}' clicked at {mouse_pos}")
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    return True
            # For rectangle, use the rect collision check
            elif self.num_of_side == 4 and self.get_rect().collidepoint(mouse_pos):
                print(f"Button '{self.text}' clicked at {mouse_pos}")
                return True
        return False

