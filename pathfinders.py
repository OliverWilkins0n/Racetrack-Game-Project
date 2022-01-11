import time
import App

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


def astar(track, start, end):
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
        if endNode.position in App.App.checkInbetween(App, currentNode.position[0], currentNode.position[1], endNode.position[0], endNode.position[1]):
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
            #[((currentNode.dx)+0, (currentNode.dy)-1), ((currentNode.dx)+0, (currentNode.dy)+1), ((currentNode.dx)-1, (currentNode.dy)+0), ((currentNode.dx)+1, (currentNode.dy)+0), ((currentNode.dx)-1, (currentNode.dy)-1), ((currentNode.dx)-1, (currentNode.dy)+1), ((currentNode.dx)+1, (currentNode.dy)-1), ((currentNode.dx)+1, (currentNode.dy)+1)]: 
                #print("New Position: ", newPosition)
                # Get node position
                nodePosition = (currentNode.position[0] + (newPosition[0]), currentNode.position[1] + (newPosition[1]))
                
                #print("Node Position: ", nodePosition)
                #time.sleep(1)
                # check to see if position is on track
                if nodePosition[0] > (len(track) - 1) or nodePosition[0] < 0 or nodePosition[1] > (len(track[len(track)-1]) -1) or nodePosition[1] < 0:
                    continue

                # Make sure the position is not grass
                if track[nodePosition[0]][nodePosition[1]] != 0:
                    continue

               # xVelocity = currentNode.dx + newPosition[0]
               # yVelocity = currentNode.dy + newPosition[1]

               #Creates new Node with the 
                newNode = Node(newPosition[0], newPosition[1], currentNode, nodePosition)
                children.append(newNode)


        # Loop through children
        for child in children:

            for closedChild in closedList:
                if child == closedChild:
                    continue

            # Create the f, g, and h values
            child.g = currentNode.g + 1 #Cost of Path from start node
            child.h = ((child.position[0] - endNode.position[0]) ** 2) + ((child.position[1] - endNode.position[1]) ** 2) #Estimates cost of cheapest path
            child.f = child.g + child.h
           # time.sleep(1)
           # print("test ", child.position, child.dx, child.dy)
            #time.sleep(0.01)
            # Child is already in the open list
            for openNode in openList:
                if child == openNode and child.g > openNode.g:
                    continue

            # Add the child to the open list
            openList.append(child)


def main():
    with open("tracks/track1.txt") as textFile:
        track = [line.split(";") for line in textFile]

    trackList = [[0 for i in range(40)] for j in range(20)]

    for i in range(len(track)):
        for j in range(40):
            if track[i][j] == "t" or track[i][j] == "s" or track[i][j] == "f":
                trackList[i][j] = 0
            else:
                trackList[i][j] = 1
    
    for i in trackList:
        print(i)

    print(trackList[18][6])
    print(trackList[4][36])
    start = (18, 6)
    end = (4, 36)
    path = astar(trackList, start, end)
    print(path)
    print("Achieved in",len(path),"moves!")


if __name__ == '__main__':
    main()