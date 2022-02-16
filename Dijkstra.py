import collections


class Node():

    def __init__(self, dx, dy, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.dx = dx
        self.dy = dy    

def dijkstra(start, end, track):
    Q = 


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
    
    for i in trackList:
        print(i)

    print(trackList[18][6])
    print(trackList[4][36])
    trackList[4][36] = "X"
    start = (18, 6)
    end = (4, 36)
    path = dijkstra(start, end, trackList)


if __name__ == '__main__':
    main()