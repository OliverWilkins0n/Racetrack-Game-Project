import collections
from email.errors import StartBoundaryNotFoundDefect
import queue
import time
import App
import track

###   PROBLEMS  
###   Staring first move with 2 y Velocity

class Node():

    def __init__(self, dx, dy, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

        self.dx = dx
        self.dy = dy    

    def bfs1(start, end, grid): 
        visited = []
        path = [(start, [start])]
        startNode = Node(0, 0, None, start)
        queue = [(startNode)]
        #visited.append([startNode])
        visited.append(start) 
        while queue:
        # print("Queue: ", queue)
            vertex, path1 = path.pop(0)
            m = queue.pop(0)
            #currentNode = m.position
            x = m.position[0]
            y = m.position[1]
            pos = x, y
        # print("x, y: ",x,y)
            #print(m, end = " ")
            for neighbour in Node.get_neighbours(pos, grid, m.dx, m.dy):
            # print("Neighbour: ", neighbour)
                #if Node(0, 0, m.position, neighbour) not in visited and grid[neighbour[0]][neighbour[1]] != 1:
            # print("Neighbour Loop: ", neighbour)
                if neighbour not in visited and grid[neighbour[0]][neighbour[1]] != 1:
                    #visited.append(Node(0, 0, m.position, neighbour))
                    dx = neighbour[0] - x
                    dy = neighbour[1] - y
                    print("DX, DY: ", dx, dy)
                    visited.append(neighbour)
                    path.append((pos, path1 + [pos]))
                    #path.append((pos, path1 + [pos]))
                    queue.append(Node(dx, dy, m.position, neighbour))
                if neighbour[0] == end[0] and neighbour[1] == end[1]:
                    return path + [end]





    def get_neighbours(node, grid, dx, dy):
        neighbours = list()
    # print("DX DY: ",dx, dy)
        #for n in [(node[0]+dx, node[1]), (node[0]-dx, node[1]), (node[0], node[1]+dy), (node[0], node[1]-dy)]:
        #for n in [(dx+1, dy), (dx-1, dy), (dx, dy+1), (dx, dy-1)]:
        for n in [(dx-1, dy-1),(dx, dy-1),(dx+1, dy-1), (dx-1, dy), (dx, dy), (dx+1, dy), (dx-1, dy+1),(dx, dy+1),(dx+1, dy+1)]:
            x = n[0] + node[0]
            y = n[1] + node[1]
            pos = (x, y)
            print("X, Y: ", x, y)
            if x < 0 or y < 0:
                pass
            elif x >= 20 or y >= 40:
                pass
            elif grid[x][y] == 1:
                pass
            else:
            # print("Neighbours: ", x, y)
                neighbours.append(pos)
    # print("1: ",neighbours)
        return neighbours


    def astar(track, CURRENTTRACK, start, end):
        firstMove = True

        # Create start and end node
        startNode = Node(0, 0, None, start)
        startNode.g = startNode.h = startNode.f = 0
        endNode = Node(0, 0, None, end)
        endNode.g = endNode.h = endNode.f = 0

        # Initialize both open and closed list
        openList = []
        closedList = []

        # Add the start node
        openList.append(startNode)

        # Loop until path is found
        while len(openList) > 0:

            # Get the current node
            currentNode = openList[0]
            currentIndex = 0
            for index, item in enumerate(openList):
                if item.f < currentNode.f:
                    currentNode = item
                    currentIndex = index

            openList.pop(currentIndex)
            closedList.append(currentNode)
            print("Current: ", currentNode.position, " dx: ", currentNode.dx, "dy: ", currentNode.dy)
            #time.sleep(1)

            #Check to make sure that the car did not shoot across the finish point by checking all points it crossed in last move
            if endNode.position in Node.getCoordsBetweenPoints(Node, currentNode.position[0], currentNode.position[1], endNode.position[0], endNode.position[1]):
                path = []
                print("Path Found!")
                current = currentNode
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                return path[::-1] # reversed

            #Check to see if car is already in the end position
            if currentNode.position == endNode.position:
                path = []
                current = currentNode
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                return path[::-1] # reversed

            # Create Children
            children = []

            if firstMove:
                #newPosition is all the possible new positions with the current velocity availble to move to
                for newPosition in [(currentNode.dx-1, currentNode.dy-1),(currentNode.dx, currentNode.dy-1),(currentNode.dx+1, currentNode.dy-1), (currentNode.dx-1, currentNode.dy), (currentNode.dx, currentNode.dy), (currentNode.dx+1, currentNode.dy), (currentNode.dx-1, currentNode.dy+1),(currentNode.dx, currentNode.dy+1),(currentNode.dx+1, currentNode.dy+1)]:
                    validMove = True
                    # Get node position
                    nodePosition = (currentNode.position[0] + (newPosition[0]), currentNode.position[1] + (newPosition[1]))
                    
                    # check to see if position is on track
                    if nodePosition[0] > (len(track) - 1) or nodePosition[0] < 0 or nodePosition[1] > (len(track[len(track)-1]) -1) or nodePosition[1] < 0:
                        continue

                    # Make sure the position is not grass
                    if track[nodePosition[0]][nodePosition[1]] != 0:
                        continue

                    #Gets All the coords between its current position and the next node, Rounded to the closest int
                    coordsBetween = Node.getCoordsBetweenPoints(Node, currentNode.position[1], currentNode.position[0], nodePosition[1], nodePosition[0])
                    #Testing
                    #print("Current Node:", currentNode.position, " New Node: ", nodePosition)
                    #print("Between these two points: ", coordsBetween)
                    #for i in range(0, len(coordsBetween)-1):
                    #    if track[coordsBetween[i][0]][coordsBetween[i][1]] == 1:
                    #        validMove = False

                    if Node.checkAllPoints(Node, coordsBetween, CURRENTTRACK) == "g":
                        print("Current Pos: ",currentNode.position, " New Pos: ", nodePosition)
                        validMove = False
                            
                #Creates new Node with the
                    if validMove: 
                        newNode = Node(newPosition[0], newPosition[1], currentNode, nodePosition)
                       # print("New Node: ", newNode)
                        children.append(newNode)


            # Loop through children
            for child in children:

                for closedChild in closedList:
                    if child == closedChild:
                        continue

                # Create the f, g, and h values
                child.g = currentNode.g + 1 #Cost of Path from start node
                dx = (child.position[0] - endNode.position[0])
                dy = (child.position[1] - endNode.position[1])
                #Works better then previous heuristic
                child.h = (dx * dx + dy * dy) ** 0.5
                #child.h = 1
                #child.h = ((dx * dx)**2 + (dy * dy)**2) 
                
                #child.h = ((child.position[0] - endNode.position[0]) ** 2) + ((child.position[1] - endNode.position[1]) ** 2) #Estimates cost of cheapest path
                child.f = child.g + child.h

                # Child is already in the open list
                for openNode in openList:
                    if child == openNode and child.g > openNode.g:
                        continue

                # Add the child to the open list
                openList.append(child)

    def loadTrack():
        with open("tracks/Working1.txt") as textFile:
            track = [line.split(";") for line in textFile]

        trackList = [[0 for i in range(40)] for j in range(20)]

        for i in range(len(track)):
            for j in range(40):
                if track[i][j] == "t" or track[i][j] == "s" or track[i][j] == "f":
                    trackList[i][j] = 0
                else:
                    trackList[i][j] = 1

        return trackList

    def getCoordsBetweenPoints(self, initX, initY, x, y):
        xSpacing = (x - initX) / 9
        ySpacing = (y - initY) / 9
        
        return [[(initX + i * xSpacing), (initY + i * ySpacing)]
                for i in range(1, 9)]

    def checkPos(self, x, y, CURRENTTRACK):

        if track.Track.getGridWithCoords(App, CURRENTTRACK, x, y) == 'g':
            return 'g'
        elif track.Track.getGridWithCoords(App, CURRENTTRACK, x, y) == "f":
            return 'f'
        else:
            return 't'
    
    def checkAllPoints(self, coords, CURRENTTRACK):
        count = 0
        for coord in coords:
            if count == 0:
                count += 1
                pass
            else:
                if Node.checkPos(Node, coord[0]*25, coord[1]*25, CURRENTTRACK) == "g":
                    return 'g'
                elif Node.checkPos(Node, coord[0]*25, coord[1]*25, CURRENTTRACK) == 'f':
                    pass
                else:
                    pass
    
    #for i in trackList:
    #    print(i)
#
 #   print(trackList[18][6])
  ##  print(trackList[4][36])
  #  start = (18, 6)
  #  end = (4, 36)
  #  path = Node.astar(trackList, start, end)
  #  print(path)
  #  print("Achieved in",len(path),"moves!")


#if __name__ == '__main__':
#    main()