class Node():

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(track, start, end):

    # Create start and end node
    startNode = Node(None, start)
    startNode.g = startNode.h = startNode.f = 0
    endNode = Node(None, end)
    endNode.g = endNode.h = endNode.f = 0

    # Initialize both open and closed list
    openList = []
    closedList = []

    # Add the start node
    openList.append(startNode)

    # Loop until you find the end
    while len(openList) > 0:

        # Get the current node
        currentNode = openList[0]
        currentIndex = 0
        for index, item in enumerate(openList):
            if item.f < currentNode.f:
                currentNode = item
                currentIndex = index

        # Pop current off open list, add to closed list
        openList.pop(currentIndex)
        closedList.append(currentNode)

        # Found the goal
        if currentNode == endNode:
            path = []
            current = currentNode
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Create Children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

            # Get node position
            nodePosition = (currentNode.position[0] + new_position[0], currentNode.position[1] + new_position[1])

            # check to see if position is on track
            if nodePosition[0] > (len(track) - 1) or nodePosition[0] < 0 or nodePosition[1] > (len(track[len(track)-1]) -1) or nodePosition[1] < 0:
                continue

            # Make sure the position is not grass
            if track[nodePosition[0]][nodePosition[1]] != 0:
                continue

            # Create new node
            new_node = Node(currentNode, nodePosition)

            children.append(new_node)

        # Loop through children
        for child in children:

            for closedChild in closedList:
                if child == closedChild:
                    continue

            # Create the f, g, and h values
            child.g = currentNode.g + 1
            child.h = ((child.position[0] - endNode.position[0]) ** 2) + ((child.position[1] - endNode.position[1]) ** 2)
            child.f = child.g + child.h

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
    
    print(trackList)
    for i in trackList:
        print(i)
    print(trackList[18][6])
    print(trackList[4][36])
    start = (18, 6)
    end = (4, 36)
    path = astar(trackList, start, end)
    print(path)

if __name__ == '__main__':
    main()