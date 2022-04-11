import pygame
from pygame import surface
from pygame.event import post
from pygame.locals import *
import button
import car
from grid import Grid
import track
from pathfinders import *

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
        App.end = False

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
        App.middleImg = pygame.image.load("imgs/middle.png")

        App.playAgainImg = pygame.image.load("imgs/playagain.png")
        App.astarImg = pygame.image.load("imgs/astar.png")
        App.bfsImg = pygame.image.load("imgs/bfs.png")


        
        #Creating Instances of Buttons
        App.upB = button.Button(1100,500, upImg, 1)
        App.topLeftB = button.Button(1050, 500, self.topLeftImg, 1)
        App.leftB = button.Button(1050, 550, self.leftImg, 1)
        App.bottomLeftB = button.Button(1050, 600, self.bottomLeftImg, 1)
        App.bottomB = button.Button(1100, 600, self.bottomImg, 1)
        App.bottomRightB = button.Button(1150, 600, self.bottomRightImg, 1)
        App.rightB = button.Button(1150, 550, self.rightImg, 1)
        App.topRightB = button.Button(1150, 500, self.topRightImg, 1)
        App.MiddleB = button.Button(1100, 550, self.middleImg, 1)
        App.playAgainB = button.Button(300, 500, self.playAgainImg, 2)
        App.astarB = button.Button(300, 695, self.astarImg, 1)
        App.bfsB = button.Button(375, 695, self.bfsImg,1)


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

    def gameOverScreen(self):
        #App().run(end)
        #self.screen.fill((0,0,0))
        App.counterText = Text("Moves Took: "+str(self.raceCar.moves), 22, (255,255,125), pos=(610, 600))
        App.counterText.draw()
        App.end = True

    def restart(self):
        startX, startY = self.getStartGrid()
        self.raceCar.rect.x = startX
        self.raceCar.rect.y = startY
        self.raceCar.dx = 0
        self.raceCar.dy = 0
        self.raceCar.moves = 0
        self.screen.fill((0,0,0))
        self.controller()
        self.draw()
        

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

    def getFinishLine(self):
        xList, yList = track.Track.getGridWithProperty(self, self.CURRENTTRACK, "f")
        midx = len(xList)//2
        midy = len(yList)//2
        return yList[midy], xList[midx]

    def checkPos(self, x, y):

        #If car goes off screen restarts the car to starting pos
        if x > 1000 or y > 500 or x < 0 or y < 0:
            startX, startY = self.getStartGrid()
            self.raceCar.rect.x = startX
            self.raceCar.rect.y = startY
            self.raceCar.dx = 0
            self.raceCar.dy = 0
            self.raceCar.moves = 0
            self.draw()
            return "OK"
        #Car on grass can only move 1 grid per move
        elif track.Track.getGridWithCoords(App, self.CURRENTTRACK, x, y) == 'g':
            self.raceCar.dx = 0
            self.raceCar.dy = 0
            print('g')
            return 'g'

        #Check to see if car has reached the finish line
        elif track.Track.getGridWithCoords(App, self.CURRENTTRACK, x, y) == "f":
            #Add What happens when reaching the finish line
            #Display the amount of moves it took to finish.
            self.gameOverScreen()
            #print("FINISHED")
            return 'f'
    
    def checkAllPoints(self, coords):
        count = 0
        for coord in coords:
            if count == 0:
                count += 1
                pass
            else:
                if self.checkPos(coord[0]*25, coord[1]*25) == "OK":
                    pass
                elif self.checkPos(coord[0]*25, coord[1]*25) == 'g':
                    startX, startY = self.getStartGrid()
                    self.raceCar.rect.x = startX
                    self.raceCar.rect.y = startY
                    self.raceCar.dx = 0
                    self.raceCar.dy = 0
                    self.raceCar.moves = 0
                elif self.checkPos(coord[0]*25, coord[1]*25) == 't':
                    return 't'
                elif self.checkPos(coord[0]*25, coord[1]*25) == 'f':
                    self.raceCar.dx = 0
                    self.raceCar.dy = 0
                    self.raceCar.rect.x = coord[0]*25
                    self.raceCar.rect.y = coord[1]*25
                    break


    def getCoordsBetweenPoints(self, initX, initY, x, y):
        xSpacing = (x - initX) / 9
        ySpacing = (y - initY) / 9
        return [[(initX + i * xSpacing)//25, (initY + i * ySpacing)//25]
                for i in range(1, 9)]
    
#    def checkInbetween(self, initX, initY, x, y):
#        xSpacing = (x - initX) // 4
#        ySpacing = (y - initY) // 4
#        return [[(initX + i * xSpacing), (initY + i * ySpacing)]
#                for i in range(1, 4)]

    def moveCar(self, dx, dy):
        initX = self.raceCar.rect.x
        initY = self.raceCar.rect.y
        self.raceCar.rect.x -= (dx*self.GRIDSIZE)
        self.raceCar.rect.y -= (dy*self.GRIDSIZE)
        self.raceCar.moves += 1
        self.checkAllPoints(self.getCoordsBetweenPoints(initX, initY, self.raceCar.rect.x, self.raceCar.rect.y))
        coords = [self.raceCar.rect.x//25, self.raceCar.rect.y//25]
        if self.checkPos(coords[0]*25, coords[1]*25) == 'f':
            self.gameOverScreen()
        self.draw()

    def moveCar1(self, dx, dy):
        initX = self.raceCar.rect.x
        initY = self.raceCar.rect.y
        self.raceCar.rect.x -= (dx*self.GRIDSIZE)
        self.raceCar.rect.y -= (dy*self.GRIDSIZE)
        self.raceCar.moves += 1
        coords = [self.raceCar.rect.x//25, self.raceCar.rect.y//25]
        if self.checkPos(coords[0]*25, coords[1]*25) == 'f':
            self.gameOverScreen()
            print("Real Moves: ", self.raceCar.moves)
        self.draw()

    def controller(self):
        #Checks to see if the car is out of bounds or on the grass
        #Car Controls
        #if App.end == False:  
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

            if App.MiddleB.draw(App.screen):
                self.moveCar(self.raceCar.dx, self.raceCar.dy)

            if App.astarB.draw(App.screen):
                start = self.getStartGrid()
                end = self.getFinishLine()
                startpos = [1, 1]
                #X and Y positions are switched in the path finder as it loads the track into a 2d array
                startpos[0] = start[1]//25
                startpos[1] = start[0]//25
                path = Node.astar(Node.loadTrack(), self.CURRENTTRACK,startpos, end)
                print(path)

                #Finds the Difference in the x and y from each move in the path
                #From this it finds out what the dx and dy would have to be for this move to have occured
                difList = path
                for i in range(len(path)-1):

                    #difList[i] = ((path[i+1][1] - path[i][1]), path[i+1][0] - path[i][0]) 
                    difList[i] = (path[i][1] - path[i+1][1], (path[i][0] - path[i+1][0]))
                
                print(difList)
                #Move the car with the moves from difList, 1 second sleep to visualise the Moves
                for move in difList:
                    self.moveCar1(move[0], move[1])
                    time.sleep(1)

            if App.bfsB.draw(App.screen):
                start = self.getStartGrid()
                end = self.getFinishLine()
                startpos = [1,1]
                endpos = [0,0]
                startpos[0] = start[1]//25
                startpos[1] = start[0]//25
                #endpos[0] = end[0]//25
                #endpos[1] = end[1]//25
                path = Node.bfs1(startpos, end, Node.loadTrack())
                #######FORMAT THE List Correctly
                print("The Path: ", path)
                thePath = path[-2]
                fixedPath = []
                for elem in thePath:
                    fixedPath.append(elem)
                fixedPath.pop(0)
                thePath = fixedPath[0]
                thePath.pop(0)
                #################################
                ##########Convert the Coordinates Into Moves##########
                thePath.append(end)
                print("Path: ", thePath)
                difList = thePath
                for i in range(len(thePath)-1):

                    #difList[i] = ((thePath[i+1][1] - thePath[i][1]), thePath[i+1][0] - thePath[i][0]) 
                    difList[i] = (thePath[i][1] - thePath[i+1][1], (thePath[i][0] - thePath[i+1][0]))
                
                print(difList)
                for move in difList:
                    self.moveCar1(move[0], move[1])
                    time.sleep(1)
                ######################################################

            if App.playAgainB.draw(App.screen):
                self.restart()
                    


if __name__ == "__main__":
    App().run()