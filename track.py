import pygame
import os
import grid

class Track():
    def __init__(self, screen):
        self.screen = screen
        self.currentTile = None
        self.trackSurface = self._loadData()
        self.inner = []

    def _loadData(self):
        self.inner = []
        #Reads lines of txt file
        with open("tracks/track1.txt", "r") as f:
            Lines = f.readlines()
            Lines = [i.strip() for i in Lines if len(i.strip()) > 0]
        id = 0
        #Creates new list after each ; then joins them together
        for i , line in enumerate(Lines):
            temp = line.split(";")
            temp = [i.strip() for i in temp if len(i.strip()) > 0]
            #Creates the grids
            for j, elem in enumerate(temp):
                newGrid = grid.Grid(id, j, i, elem)
                self.inner.append(newGrid)
                id += 1
        return self.inner

    def draw(self, surface, currentTrack):
        if len(currentTrack) == 0:
            print("no Track")
        for elem in currentTrack:
            surface.blit(elem.image, elem.rect)
            #self.screen.blit(elem.image, elem.react)