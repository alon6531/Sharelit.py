import pygame

from Client_side.App.AppEngine import *  # Assuming GameEngine is a module that contains the GameEngine class

class App:
    def __init__(self, window, status, client, width=1240, height=650):
        self.window = window
        self.status = status
        self.client = client
        game = AppEngine(client, status)
        game.run()

