import collections


class Node():

    def __init__(self, dx, dy, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.dx = dx
        self.dy = dy    

def bfs1(start, end, grid):
        print("asdasdasdasd ",grid[5][36])
        queue = collections.deque([[start]])
        #queue = []
        seen = set([start])
        print("Seen: ", seen)
        while queue:
            path = queue.popleft()
            x, y = path[-1]
            node = (x, y)
            if x == end[0] and y == end[1]:
                return path
            for x2, y2 in get_neighbours(node, grid):
            #for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)):
                if grid[x2][y2] != 1 and (x2, y2) not in seen:
                    print("Current Pos: ", x2, y2)
                    queue.append(path + [(x2, y2)])
                    seen.add((x2, y2))


def get_neighbours(node, grid):
    neighbours = list()
    for n in [(node[0]+1, node[1]), (node[0]-1, node[1]), (node[0], node[1]+1), (node[0], node[1]-1)]:
        x = n[1]
        y = n[0]
        if grid[x][y] == 1:
            pass
        else:
            neighbours.append(n)
    return neighbours



def main():
    with open("tracks/1111.txt") as textFile:
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
    print(path)
    print("Path found in ", len(path), " Moves!")


if __name__ == '__main__':
    main()