import pygame

from Client_side.App.GameObject import *

class Story(GameObject):
    def __init__(self, x, y, width=40, height=40, color=(255, 0, 0), description="Story Entity"):
        super().__init__(x, y, width, height, color, "", "../Assets/star.png")
        self.description = description


    def get_description(self):
        return self.description



