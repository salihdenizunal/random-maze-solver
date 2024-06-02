from MazeGenerator import MazeGenerator
from Pawn import Pawn
from Maze import Maze
from RandomNumberGenerator import RandomNumberGenerator
import matplotlib.pyplot as plt

class DynamicMaze(Maze):
    def __init__(self, rows = 15, cols = 15):
        super().__init__(rows, cols)
        mazeGenerator = MazeGenerator(rows, cols)
        mazeGenerator.generateMaze()
        self.walls = mazeGenerator.maze.walls
        self.vertices = mazeGenerator.maze.vertices
        self.pawn = Pawn((0,0), (rows-1, cols-1), self.copy())
        
        # Generate a random starting value for the lcg2 function call
        self.randomNumberGenerator = RandomNumberGenerator()
        
    def __removeWall(self, wall):
        if self.hasWall(wall):
            self.walls.remove(wall)

    def __addWall(self, wall):
        if not self.hasWall(wall):
            self.walls.append(wall)

    def __createsChain(self, wall):
        # Unpack the wall coordinates
        (start, end) = wall

        # Get the neighbors of the start and end vertices
        start_neighbors = self.getNeighborVertices(start)
        end_neighbors = self.getNeighborVertices(end)

        # It checks if adding this wall would isolate either the start or end vertex.
        # If a vertex has only one neighbor (including the other end of the wall being added),
        # adding this wall would isolate it, which is undesirable. In this case, the method 
        # returns True, indicating that adding this wall would create a chain.
        if len(start_neighbors) == 1 or len(end_neighbors) == 1:
            return True

        # Verify if the start and end vertices are already connected by other walls.
        # If they are, then adding this wall won't create a chain. The method checks
        # if any neighbor of the start vertex is the same as any neighbor of the end vertex.
        # If such a neighbor exists, it means the start and end vertices are already connected,
        # and hence adding this wall won't create a chain.
        start_connected = any(neigh in start_neighbors for neigh in end_neighbors)
        if start_connected:
            return False  # Adding this wall won't create a chain

        # If the start and end vertices are not already connected, the method examines
        # if adding this wall would create a chain for the start vertex. It checks if all
        # neighbors of the start vertex already have walls between them and the start vertex.
        # If so, adding this wall would isolate the start vertex from the rest of the maze,
        # creating a chain.
        start_chain = all(self.hasWall((start, neigh)) for neigh in start_neighbors)
        if start_chain:
            return True  # Adding this wall will create a chain

        # Similarly, if adding the wall wouldn't create a chain at the start vertex,
        # it checks if it would create a chain at the end vertex. It examines if
        # all neighbors of the end vertex already have walls between them and the end vertex.
        # If so, adding this wall would isolate the end vertex from the rest of the maze,
        # creating a chain.
        end_chain = all(self.hasWall((end, neigh)) for neigh in end_neighbors)
        if end_chain:
            return True  # Adding this wall will create a chain

        return False  # Adding this wall won't create a chain

    def updateMaze(self):
        # Add or remove walls        
        row = (self.randomNumberGenerator.generate() % (self.getRows() - 1))
        col = (self.randomNumberGenerator.generate() % (self.getCols() - 1))

        buffer = min(self.getRows(), self.getCols())

        start = (row, col)
        # Randomly select the direction of the end vertex (up, down, left, right)
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        direction = directions[self.randomNumberGenerator.generate() % 4]
        
        end = (start[0] + direction[0], start[1] + direction[1])
        wall = (start, end)
        if self.hasWall(wall):
            if len(self.walls) + buffer < len(self.vertices): return
            self.__removeWall(wall)  # Remove wall

            calculatedPath = self.pawn.findPath()
            if calculatedPath is None:
                self.__addWall(wall)
            else:
                self.pawn.setPath(calculatedPath)
                self.pawn.setMaze(self.copy())
        else:
            if len(self.walls) - buffer > len(self.vertices): return
            if self.__createsChain(wall): return
            self.__addWall(wall)  # Add wall

            calculatedPath = self.pawn.findPath()
            if calculatedPath is None:
                self.__removeWall(wall)
            else:
                self.pawn.setPath(calculatedPath)
                self.pawn.setMaze(self.copy())

    def plot(self):
        plt.clf()
        super().plot()
        self.pawn.plot()
        # Set plot properties
        plt.axis('square')
        plt.draw()
        plt.pause(0.001)  # Add a small pause to allow for plot updates
        