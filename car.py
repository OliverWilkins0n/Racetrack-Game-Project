import pygame
import App

class Car(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("imgs/car.png").convert_alpha()
        self.image = img
        self.rect = self.image.get_rect()
        self.dx = 0
        self.dy = 0
