import pygame
from pygame import surface
from pygame.event import post
from pygame.locals import *
import button
from grid import Grid
import track
import os

import pygame
import os
import grid



class Text:
    def __init__(self, text, fontSize, fontColour, pos, **options):
        self.text = text
        self.pos = pos
        self.fontName = None
        self.fontSize = fontSize
        self.fontColour = fontColour
        self.set_font()
        self.render()

    def set_font(self):
        self.font = pygame.font.Font(pygame.font.get_default_font(), self.fontSize)
    
    def render(self):
        self.img = self.font.render(self.text, True, self.fontColour)
        self.rect = self.img.get_rect()
        self.rect.topleft = self.pos

    def draw(self):
        App.screen.blit(self.img, self.rect)


class App:

    def __init__(self):
        #Create the display
        HEIGHT = 720
        WIDTH = 1280
        pygame.init()
        flags = RESIZABLE
        self.clock = pygame.time.Clock()
        App.screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)

        # 1. Create the track class  2. Loads track data from text file and stores it in variable self.CURRENTTRACK
        self.track = track.Track(self.screen)
        self.CURRENTTRACK = track.Track._loadData(self)

        #Load Button Images
        upImg = pygame.image.load('imgs/up.jpg')
        App.topLeftImg = pygame.image.load("imgs/topLeft.png")
        App.leftImg = pygame.image.load("imgs/left.png")
        App.bottomLeftImg = pygame.image.load("imgs/bottomleft.png")
        App.bottomImg = pygame.image.load("imgs/bottom.png")
        App.bottomRightImg = pygame.image.load("imgs/bottomright.png")
        App.rightImg = pygame.image.load("imgs/right.png")
        App.topRightImg = pygame.image.load("imgs/topright.png")

        
        #Creating Instances of Buttons
        App.upB = button.Button(1100,500, upImg, 1)
        App.topLeftB = button.Button(1050, 500, self.topLeftImg, 1)
        App.leftB = button.Button(1050, 550, self.leftImg, 1)
        App.bottomLeftB = button.Button(1050, 600, self.bottomLeftImg, 1)
        App.bottomB = button.Button(1100, 600, self.bottomImg, 1)
        App.bottomRightB = button.Button(1150, 600, self.bottomRightImg, 1)
        App.rightB = button.Button(1150, 550, self.rightImg, 1)
        App.topRightB = button.Button(1150, 500, self.topRightImg, 1)


        #Create text
        App.headerText = Text("Racetrack Game", 22, (255,255,255), pos=(550, 10),)

        App.running = True

    def run(self):
        #Instance Handler
        self.drawInit = True
        while App.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    App.running = False

            #Draw The Control Buttons
            if App.upB.draw(App.screen):
                print("UP")
                self.draw()
            App.topLeftB.draw(App.screen)
            App.leftB.draw(App.screen)
            App.bottomLeftB.draw(App.screen)
            App.bottomB.draw(App.screen)
            App.bottomRightB.draw(App.screen)
            App.rightB.draw(App.screen)
            App.topRightB.draw(App.screen)
            if self.drawInit:
                self.draw()
                self.drawInit = False
        #    App.headerText.draw()
        #    pygame.display.update()
        pygame.quit()

    def draw(self):
        #Draws the track
        track.Track.draw(self, self.screen, self.CURRENTTRACK)
        
        pygame.display.update()



if __name__ == "__main__":
    App().run()