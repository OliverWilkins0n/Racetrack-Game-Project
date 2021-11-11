import pygame
#import App

class Grid():
    def __init__(self, id, x, y, type):
        GRIDSIZE = 25
        self.id = id
        self.x = int(x)
        self.y = int(y)
        self.type = type
        #Gets Image for Type of Grid
        if type == "g":
            filename = "imgs/grass.png"
        elif type == "t":
            filename = "imgs/track.png"
        elif type == "s":
            filename = "imgs/start.png"
        elif type == "f":
            filename = "imgs/finish.png"
        else:
            print("Unknown grid type!")

        self.rect = pygame.Rect(self.x * GRIDSIZE, self.y * GRIDSIZE, GRIDSIZE, GRIDSIZE)
        if type == "g" or type == "t" or type == "s" or type == "f":
            self.image = pygame.image.load(filename)
            self.image = pygame.transform.scale(self.image, (GRIDSIZE, GRIDSIZE))