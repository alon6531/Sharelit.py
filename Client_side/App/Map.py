import pygame
from Client_side.App.GameObject import GameObject

class Map(GameObject):
    def __init__(self, x, y, width, height, image_path):
        super().__init__(x, y, width, height, (0, 0, 0))  # No color needed since it's an image
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))

    def render(self, screen, camera):
        # Draw the map relative to the camera position
        screen.blit(self.image, (self.x - camera.x, self.y - camera.y))

    def update(self):
        # No update logic for a static map, but you can add effects here
        pass