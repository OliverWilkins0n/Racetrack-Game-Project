import collections


class Node():

    def __init__(self, dx, dy, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.dx = dx
        self.dy = dy


######NOT USING#################################################################
def bfs1222(start, end, grid):
        print(grid[18][7])
        queue = collections.deque([[start]])
        startNode = Node(0, 0, None, start)
        nodeQueue = [(startNode)]
        seen = set([start])
        while queue:
            path = queue.popleft()
            nodePath = nodeQueue.pop(0)
            print("Node Path: ", nodePath.position)
            x, y = path[-1]
            node = [x,y]
            #print("THE NODE: ", node)
            if x == end[0] and y == end[1]:
                return path
           #x2, y2 is the new dx and dy for that move.
           # for x2, y2 in [(nodePath.dx-1, nodePath.dy-1),(nodePath.dx, nodePath.dy-1),(nodePath.dx+1, nodePath.dy-1), (nodePath.dx-1, nodePath.dy), (nodePath.dx, nodePath.dy), (nodePath.dx+1, nodePath.dy), (nodePath.dx-1, nodePath.dy+1),(nodePath.dx, nodePath.dy+1),(nodePath.dx+1, nodePath.dy+1)]:
            for x2, y2 in get_neighbours(node, grid, 0, 0):
                valid = True
               # print("x2: ",x2,"y2: ",y2)
                if valid:
                    #Where this new Node that is being explored would be positioned
                    nodePosition = (nodePath.position[0] + x2, nodePath.position[1] + y2)
                    #Make sure that this position is on the track and that it hasn't already been explored
                    print("nodePosition[0]: ", nodePosition[0])
                    print("nodePosition[1]: ", nodePosition[1])
                    if x2 < len(grid[0]) and y2 < len(grid) and x2 >= 0 and y2 >= 0:
                        if grid[nodePosition[1]][nodePosition[0]] != 1 and (nodePosition[1], nodePosition[0]) not in seen:
                            #Add the Current Position to the queue
                            queue.append(path + [(nodePosition[1], nodePosition[0])])
                        # queue.append(path + [(x2, y2)])
                            nodeQueue.append(Node(x2, y2, nodePath.position, nodePosition))
                            seen.add((nodePosition[1], nodePosition[0]))



def backtrace(parent, start, end):
    path = [end]
    while path[-1] != start:
        #print(parent[path[-1]])
        path.append(parent[path[-1]])
    path.reverse()
    print("The Path is: ",path)
    return path

def bfs123(start, end, grid): #Just keeping velocity at 0,0 atm when creating nodes as not using velocity atm
    # also only using 4 directions
    parent = {}
    visited = []
    startNode = Node(0, 0, None, start)
    queue = [(startNode)]
    #visited.append([startNode])
    visited.append(start) 
    while queue:
       # print("Queue: ", queue)
        m = queue.pop(0)
        #currentNode = m.position
        x = m.position[0]
        y = m.position[1]
        pos = x, y
        #print("x, y: ",x,y)
        #print(m, end = " ")
        for neighbour in get_neighbours(pos, grid, 0, 0):
           # print("Neighbour: ", neighbour)
            #if Node(0, 0, m.position, neighbour) not in visited and grid[neighbour[0]][neighbour[1]] != 1:
            if neighbour[0] == end[0] and neighbour[1] == end[1]:
                print("Found")
                return backtrace(parent, start, end)
            if neighbour not in visited and grid[neighbour[0]][neighbour[1]] != 1:
                #visited.append(Node(0, 0, m.position, neighbour))
                visited.append(neighbour)
                originalPos = m.position
                parent[neighbour] = originalPos
                queue.append(Node(0, 0, m.position, neighbour))
                

def bfs111(start, end, grid): #WORKING WITHOUT SHOWING PATH AT END
    # also only using 4 directions
    visited = []
    startNode = Node(0, 0, None, start)
    queue = [(startNode)]
    #visited.append([startNode])
    visited.append(start) 
    while queue:
       # print("Queue: ", queue)
        m = queue.pop(0)
        #currentNode = m.position
        x = m.position[0]
        y = m.position[1]
        pos = x, y
        print("x, y: ",x,y)
        #print(m, end = " ")
        for neighbour in get_neighbours(pos, grid, 0, 0):
           # print("Neighbour: ", neighbour)
            #if Node(0, 0, m.position, neighbour) not in visited and grid[neighbour[0]][neighbour[1]] != 1:
            if neighbour not in visited and grid[neighbour[0]][neighbour[1]] != 1:
                #visited.append(Node(0, 0, m.position, neighbour))
                visited.append(neighbour)
                queue.append(Node(0, 0, m.position, neighbour))
            if neighbour[0] == end[0] and neighbour[1] == end[1]:
                return m

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
        for neighbour in get_neighbours(pos, grid, m.dx, m.dy):
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
    
#    for i in trackList:
#        print(i)
#
#    print(trackList[18][6])
#    print(trackList[4][36])
    #trackList[4][36] = "X"
    start = (18, 6)
    end = (4, 36)
    path = bfs1(start, end, trackList)
    thePath = path[-2]
    fixedPath = []
    for elem in thePath:
        fixedPath.append(elem)

    fixedPath.pop(0)
    thePath = fixedPath[0]
    thePath.pop(0)
    print("THe Path: ", thePath)



if __name__ == '__main__':
    main()
