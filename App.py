import pygame
from pygame import surface
from pygame.event import post
from pygame.locals import *
import button
import car
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

    def delete(self):
        App.screen.blit()


class App:

    def __init__(self):
        #Create the display
        HEIGHT = 720
        WIDTH = 1280
        self.GRIDSIZE = 25
        pygame.init()
        flags = RESIZABLE
        self.clock = pygame.time.Clock()
        App.screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)

        # 1. Create the track class  2. Loads track data from text file and stores it in variable self.CURRENTTRACK
        self.track = track.Track(self.screen)
        self.CURRENTTRACK = track.Track._loadData(self)
        #Create the car
   #     carX, carY = self.getStartGrid()
   #     App.carImg = pygame.image.load("imgs/car.png").convert_alpha()
    #    App.raceCar = car.Car(carX, carY, self.screen)

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
        App.endGameText = Text("Game Over", 22, (255,255,255), pos=(550, 10),)
        App.velocityText = Text("", 22, (255,255,255), pos=(550, 10),)

        App.running = True

    def run(self):
        
        self.createCar()
        #Instance Handler
        self.drawInit = True
        while App.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    App.running = False

            #Draw The Control Buttons
            self.controller()

            if self.drawInit:
                self.draw()
                self.drawInit = False
        #    App.headerText.draw()
        #    pygame.display.update()
        pygame.quit()

    def createCar(self):
        carX, carY = self.getStartGrid()
        self.raceCar = car.Car()
        self.raceCar.rect.x = carX
        self.raceCar.rect.y = carY
        self.raceCar_list = pygame.sprite.Group()
        self.raceCar_list.add(self.raceCar)

    def draw(self):
        #Draws the track
        track.Track.draw(self, self.screen, self.CURRENTTRACK) #Draws Track
        self.raceCar_list.draw(self.screen) # Draws Car on screen
        #App.velocityText.draw()
        pygame.display.update()
    
    def getStartGrid(self):
        xList, yList = track.Track.getGridWithProperty(self, self.CURRENTTRACK, "s")
        print(xList, yList)
        midx = len(xList)//2
        midy = len(yList)//2
        return xList[midx]*25, yList[midy]*25

    def moveCar(self, dx, dy):
        initX = self.raceCar.rect.x
        initY = self.raceCar.rect.y
        self.raceCar.rect.x -= (dx*self.GRIDSIZE)
        self.raceCar.rect.y -= (dy*self.GRIDSIZE)
        #App.velocityText = Text("Velocity x: "+ str(self.raceCar.dx)+" Velocity y: "+str(self.raceCar.dy), 16, (255,255,255), pos=(200, 600),)
        #Check the new position before the car is drawn to the screen
        #self.checkAllPoints(initX, initY, self.raceCar.rect.x, self.raceCar.rect.y)
        self.checkAllPoints(self.getCoordsBetweenPoints(initX, initY, self.raceCar.rect.x, self.raceCar.rect.y))
       # self.checkPos(self.raceCar.rect.x, self.raceCar.rect.y)
        self.draw()

    def checkPos(self, x, y):
        #If car goes off screen restarts the car to starting pos
        if x > 1000 or y > 500 or x < 0 or y < 0:
            startX, startY = self.getStartGrid()
            self.raceCar.rect.x = startX
            self.raceCar.rect.y = startY
            self.raceCar.dx = 0
            self.raceCar.dy = 0
            self.draw()
            return "OK"
        #Car on grass can only move 1 grid per move
        elif track.Track.getGridWithCoords(self, self.CURRENTTRACK, x, y) == 'g':
            self.raceCar.dx = 0
            self.raceCar.dy = 0
            return 'g'
        #Check to see if car has reached the finish line
        elif track.Track.getGridWithCoords(self, self.CURRENTTRACK, x, y) == "f":
            #Add What happens when reaching the finish line
            #Display the amount of moves it took to finish.
            print("FINISHED")
            return 'f'
    
    def checkAllPoints(self, coords):
        for coord in coords:
            if self.checkPos(coord[0]*25, coord[1]*25) == "OK":
                pass
            elif self.checkPos(coord[0]*25, coord[1]*25) == 'g':
                self.raceCar.dx = 0
                self.raceCar.dy = 0
                self.raceCar.rect.x = coord[0]*25
                self.raceCar.rect.y = coord[1]*25
                print("G")
            elif self.checkPos(coord[0]*25, coord[1]*25) == 'f':
                self.raceCar.dx = 0
                self.raceCar.dy = 0
                self.raceCar.rect.x = coord[0]*25
                self.raceCar.rect.y = coord[1]*25
                print("FINISHED RACE")
                break

    def getCoordsBetweenPoints(self, initX, initY, x, y):
        xSpacing = (x - initX) / 9
        ySpacing = (y - initY) / 9
        return [[(initX + i * xSpacing)//25, (initY + i * ySpacing)//25]
                for i in range(1, 9)]

    def controller(self):
        #Checks to see if the car is out of bounds or on the grass
        #Car Controls
            
            if App.upB.draw(App.screen):
                self.raceCar.dy += 1
                self.moveCar(self.raceCar.dx, self.raceCar.dy)

            if App.topRightB.draw(App.screen):
                self.raceCar.dy += 1
                self.raceCar.dx -= 1
                self.moveCar(self.raceCar.dx, self.raceCar.dy)

            if App.leftB.draw(App.screen):
                self.raceCar.dx += 1
                self.moveCar(self.raceCar.dx, self.raceCar.dy)


            if App.bottomRightB.draw(App.screen):
                self.raceCar.dx -= 1
                self.raceCar.dy -= 1
                self.moveCar(self.raceCar.dx, self.raceCar.dy)


            if App.bottomB.draw(App.screen):
                self.raceCar.dy -= 1
                self.moveCar(self.raceCar.dx, self.raceCar.dy)


            if App.bottomLeftB.draw(App.screen):
                self.raceCar.dy -= 1
                self.raceCar.dx += 1
                self.moveCar(self.raceCar.dx, self.raceCar.dy)

                
            if App.rightB.draw(App.screen):
                self.raceCar.dx -= 1
                self.moveCar(self.raceCar.dx, self.raceCar.dy)

            if App.topLeftB.draw(App.screen):
                self.raceCar.dx += 1
                self.raceCar.dy += 1
                self.moveCar(self.raceCar.dx, self.raceCar.dy)


if __name__ == "__main__":
    App().run()