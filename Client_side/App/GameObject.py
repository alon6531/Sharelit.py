import pygame
from PIL.ImageOps import scale


class GameObject:
    def __init__(self, x, y, width, height, color=(255, 0, 0), username="", texture_path=None, tex_scale=1):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.username = username
        self.scale = tex_scale
        self.font = pygame.font.Font("../font.ttf", 30)


        # Load texture if provided
        self.texture = None
        if texture_path:
            try:
                self.texture = pygame.image.load(texture_path)
                self.texture = pygame.transform.scale(self.texture, (width * tex_scale, height * tex_scale))
            except pygame.error as e:
                print(f"Error loading texture: {e}")
                self.texture = None

    def update(self):
        """Update the logic of the object (to be implemented in derived classes)."""
        pass

    def render(self, screen, camera):
        """Render the object and its username on the screen."""
        if self.texture:
            # Draw pre-scaled texture instead of scaling every frame
            screen.blit(self.texture, (self.x - camera.x, self.y - camera.y))
        else:
            pygame.draw.rect(screen, self.color, self.get_rect().move(-camera.x, -camera.y))

        # Draw the username if it exists
        if self.username:
            text = self.font.render(self.username, True, (255, 255, 255))  # White text
            text_rect = text.get_rect(center=(self.x + int(self.width * self.scale) // 2 - camera.x, self.y - 20 - camera.y))
            screen.blit(text, text_rect)

    def get_rect(self):
        """Returns the rectangle of the object."""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def on_click(self, mouse_pos):
        pass
