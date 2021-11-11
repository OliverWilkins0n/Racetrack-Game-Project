import pygame
from pygame.locals import *

class text:

    def __init__(self, text, pos, fontSize, fontColour, **options):
        self.text = text
        self.pos = pos
        self.fontName = None
        self.fontSize = fontSize
        self.fontColour = fontColour
        self.set_font()
        self.render()

    def set_font(self):
        self.font = pygame.font.Font(self.fontName, self.fontSize)
    
    def render(self):
        self.img = self.font.render(self.text, True, self.fontColour)
        self.rect = self.img.get_rect()
        self.rect.topleft = self.pos

    def draw(self):
        App.screen.blit(self.img, self.rect)
        