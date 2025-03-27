from Client_side.App.GameObject import *


class Others(GameObject):
    def __init__(self, x, y, username, width=50, height=50, color=(0, 255, 0), speed=20):
        super().__init__(x, y, width, height, color, username,  "../assets/police.png", 2)
        self.speed = speed



