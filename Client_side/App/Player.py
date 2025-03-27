from Client_side.App.GameObject import *


class Player(GameObject):
    def __init__(self, x, y, username, width=50, height=50, color=(0, 255, 0), speed=20):
        super().__init__(x, y, width, height, color, username, "../assets/pig.png", 2)
        self.speed = speed

    def handle_input(self):
        """בדיקת קלט מהמקלדת והזזת השחקן בהתאם"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_d]:
            self.x += self.speed
        if keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_s]:
            self.y += self.speed

    def update(self):
        """עדכון מצב השחקן (כולל קלט)"""
        self.handle_input()

