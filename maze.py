#  Maze Piece Guide
#
#  Heading
#    N
#  W   E
#    S
#
#  0 [filled] - 00 filled tile
#  1 [straight] - 10 west to east straight path - 11 north to south straight path
#  2 [special area] - 20 special area opening north - 21 special area opening east - 22 special area opening south - 23 special area opening west
#  3 [corner] - 30 corner north to east - 31 corner east to south - 32 corner south to west - 33 corner west to north
#  4 [three way] - 40 three way north to south branch east - 41 three way east to west branch to south - 42 three way south to north branch west - 43 three way west to east branch north
#  5 [four way] - 50 four way connection
import random

#*Checklist for eventual graphics implementation and collision 

#Add positional values into the tile class to be displayed later (should be scalable)

#Add a "Wall" class which make up the 9 subdivisions of a maze section, each should have positional values (at: 0,0 0,1/3, 0,2/3
#                                                                    from top left to bottom right ->       1/3,0 1/3,1/3, 1/3,2/3
#                                                                                                           2/3,0 2/3,1/3, 2/3,2/3)

#Add graphical stuff after

class Tile:
    # Tile seperation pairs
    pairedWalls = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}

    def __init__(self, x, y):
        # Initialize a tile at given (x, y), starts surrounded by walls
        self.x = x
        self.y = y

        self.walls = {'N': True, 'E': True, 'S': True, 'W': True}

        self.goal = 'None'

    def hasAllWalls(self):
        # Returns true if tile still has all it's walls
        # False otherwise
        return all(self.walls.values())

    def removeWall(self, otherTile, wallPos):
        # Removes the wall between the curent (self) tile and the other tile
        self.walls[wallPos] = False
        otherTile.walls[Tile.pairedWalls[wallPos]] = False


class Maze:

    def __init__(self, yHeight, xLength):
        # Size of defined maze height (y) by length (x)
        self.lengthX = xLength
        self.heightY = yHeight

        # Defined start position at (0, 0)
        self.currentX = 0
        self.currentY = 0

        # Create 2D array to represent a map of the maze (contains tiles)
        self.mazeMap = [[Tile(x, y) for y in range(yHeight)]
                        for x in range(xLength)]

    def __str__(self):
        mazeRows = ['']
        foundStart = 'Not Found'
        foundEnd = 'Not Found'
        for y in range(self.heightY):
            mazeRow = ['']
            for x in range(self.lengthX):
                wallSections = [""]
                currentTile = self.mazeMap[x][y]
                if(currentTile.walls['N']):
                    wallSections.append("N")
                if(currentTile.walls['E']):
                    wallSections.append("E")
                if(currentTile.walls['S']):
                    wallSections.append("S")
                if(currentTile.walls['W']):
                    wallSections.append("W")
                mazeRow.append(self.tileWallsToPieceID(''.join(wallSections)))
                if(currentTile.goal.__contains__("Start")):
                    foundStart = currentTile.goal + \
                        " (" + str(x) + ", " + str(y) + ")"
                if(currentTile.goal.__contains__("End")):
                    foundEnd = currentTile.goal + \
                        " (" + str(x) + ", " + str(y) + ")"
            mazeRows.append(''.join(mazeRow))
        mazeRows.append(foundStart)
        mazeRows.append(foundEnd)

        return '\n'.join(mazeRows)

    def generateMaze(self):
        totalTiles = self.lengthX * self.heightY
        tileStack = []
        currentTile = self.tileAt(self.currentX, self.currentY)
        vistedTiles = 1
        endFound = False
        # Generate the maze by travelling through each tile starting at (0, 0)
        currentTile.goal = "Start"
        while vistedTiles < totalTiles:
            neighbours = self.validNeighbours(currentTile)
            # If there are no unvisted tiles return to previous tile
            if not neighbours:
                # Mark the first dead end tile
                if not endFound:
                    currentTile.goal = "1st End"
                    endFound = True
                currentTile = tileStack.pop()
                continue
            # Next tile is randomly picked
            direction, nextTile = random.choice(neighbours)
            currentTile.removeWall(nextTile, direction)
            tileStack.append(currentTile)
            currentTile = nextTile
            vistedTiles += 1

    def tileAt(self, x, y):
        return self.mazeMap[x][y]

    def tileWallsToPieceID(self, walls):
        # Given a set of walls, return what piece that would represent
        idValue = ' '
        if(walls == 'NESW'):
            idValue = '00 '
        elif(walls == 'NS'):
            idValue = '10 '
        elif(walls == 'EW'):
            idValue = '11 '
        elif(walls == 'ESW'):
            idValue = '20 '
        elif(walls == 'NSW'):
            idValue = '21 '
        elif(walls == 'NEW'):
            idValue = '22 '
        elif(walls == 'NES'):
            idValue = '23 '
        elif(walls == 'SW'):
            idValue = '30 '
        elif(walls == 'NW'):
            idValue = '31 '
        elif(walls == 'NE'):
            idValue = '32 '
        elif(walls == 'ES'):
            idValue = '33 '
        elif(walls == 'W'):
            idValue = '40 '
        elif(walls == 'N'):
            idValue = '41 '
        elif(walls == 'E'):
            idValue = '42 '
        elif(walls == 'S'):
            idValue = '43 '
        elif(walls == ''):
            idValue = '50 '
        else:
            # If no matching set of walls found
            print("Unknown piece found at (" +
                  self.currentX + ", " + self.currentY + ")")
            idValue = "99"

        return idValue

    def validNeighbours(self, tile):
        # Required operation to go in a certain direction
        directionDisplacement = [('N', (0, -1)),
                                 ('E', (1, 0)),
                                 ('S', (0, 1)),
                                 ('W', (-1, 0))]
        neighbours = []
        for direction, (xDirection, yDirection) in directionDisplacement:
            xFinal = tile.x + xDirection
            yFinal = tile.y + yDirection
            # A valid neighbour is identified if the final displacement is
            # Greater than 0
            # Less than max length/height
            if (0 <= xFinal < self.lengthX) and (0 <= yFinal < self.heightY):
                neighbour = self.tileAt(xFinal, yFinal)
                # Check if we have been there before
                # If not add it to the list
                # Else skip it/do nothing
                if neighbour.hasAllWalls():
                    neighbours.append((direction, neighbour))
        return neighbours


# Size Definition of the maze
height = 5
length = 6

# Maze Generation and display
generatedMaze = Maze(height, length)
generatedMaze.generateMaze()
print(generatedMaze)