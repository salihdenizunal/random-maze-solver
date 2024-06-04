from MazeGenerator import MazeGenerator
from Pawn import Pawn
from Maze import Maze
from RandomNumberGenerator import RandomNumberGenerator
import matplotlib.pyplot as plt

class DynamicMaze(Maze):
    """
    A class that represents a dynamic maze.

    Inherits from the Maze class.

    Attributes:
        walls (list): A list of walls in the maze.
        vertices (list): A list of vertices in the maze.
        pawn (Pawn): The pawn object in the maze.
        randomNumberGenerator (RandomNumberGenerator): The random number generator object.

    Methods:
        __init__(rows, cols): Initializes the DynamicMaze object.
        __removeWall(wall): Removes a wall from the maze.
        __addWall(wall): Adds a wall to the maze.
        __createsChain(wall): Checks if adding a wall would create a chain in the maze.
        updateMaze(updateFactor): Updates the maze by adding or removing walls.
        plot(): Plots the maze and the pawn.
    """

    def __init__(self, rows=12, cols=12):
        """
        Initialize the DynamicMaze object.

        Parameters:
        - rows: The number of rows in the maze. Default is 12.
        - cols: The number of columns in the maze. Default is 12.

        Returns:
        None
        """
        super().__init__(rows, cols)
        mazeGenerator = MazeGenerator(rows, cols)
        mazeGenerator.generateMaze()
        self.walls = mazeGenerator.maze.walls
        self.vertices = mazeGenerator.maze.vertices
        self.pawn = Pawn((0, 0), (rows - 1, cols - 1), self.copy())
        self.pawn.setPath(self.pawn.findPath())
        self.randomNumberGenerator = RandomNumberGenerator()

    def __removeWall(self, wall):
        """
        Remove a wall from the maze.

        Parameters:
        - wall: The wall to be removed.

        Returns:
        None
        """
        if self.hasWall(wall):
            self.walls.remove(wall)

    def __addWall(self, wall):
        """
        Add a wall to the maze.

        Parameters:
        - wall: The wall to be added.

        Returns:
        None
        """
        if not self.hasWall(wall):
            self.walls.append(wall)

    def __createsChain(self, wall):
        """
        Check if adding a wall would create a chain in the maze.
        A chain is created when a vertex becomes isolated from the rest of the maze.

        Parameters:
        - wall: The wall to be added.

        Returns:
        - True if adding the wall would create a chain, False otherwise.
        """
        # Unpack the wall coordinates
        (start, end) = wall

        # Get the neighbors of the start and end vertices
        startNeighbors = self.getNeighborVertices(start)
        endNeighbors = self.getNeighborVertices(end)

        # Check if adding this wall would isolate either the start or end vertex.
        # If a vertex has only one neighbor adding this wall would be isolating it.
        if len(startNeighbors) == 1 or len(endNeighbors) == 1:
            return True

        # Check if adding this wall would create a chain for the start vertex.
        startChain = all(self.hasWall((start, neigh)) for neigh in startNeighbors)
        if startChain:
            return True

        # Check if adding this wall would create a chain for the end vertex.
        endChain = all(self.hasWall((end, neigh)) for neigh in endNeighbors)
        if endChain:
            return True

        return False

    def updateMaze(self, updateFactor):
        """
        Update the maze by adding or removing walls.

        Parameters:
        - updateFactor: The number of walls to add or remove.

        Returns:
        None
        """
        # Update the maze by adding or removing walls
        for _ in range(updateFactor):
            # Select random row and column to add or remove walls
            row = (self.randomNumberGenerator.generate() % (self.getRows() - 1))
            col = (self.randomNumberGenerator.generate() % (self.getCols() - 1))

            start = (row, col)
            # Randomly select the direction of the end vertex (up, down, left, right)
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            direction = directions[self.randomNumberGenerator.generate() % 4]

            end = (start[0] + direction[0], start[1] + direction[1])
            wall = (start, end)
            # If the random wall already exists, remove it. Otherwise, add it.
            if self.hasWall(wall):
                self.__removeWall(wall)

                # Update the path of the pawn.
                self.pawn.setMaze(self.copy())
                calculatedPath = self.pawn.findPath()
                self.pawn.setPath(calculatedPath)
            else:
                # Check if adding this wall would create a chain in the maze.
                # If it does, skip this wall.
                if self.__createsChain(wall):
                    continue
                self.__addWall(wall)

                # Check if the pawn can still find a path after adding the wall.
                # If not, remove the wall.
                self.pawn.setMaze(self.copy())
                calculatedPath = self.pawn.findPath()
                if calculatedPath is None:
                    self.__removeWall(wall)
                    self.pawn.setMaze(self.copy())
                else:
                    # Update the path of the pawn.
                    self.pawn.setPath(calculatedPath)

    def plot(self):
        """
        Plot the maze and the pawn.

        Returns:
        None
        """
        plt.clf()
        super().plot()
        self.pawn.plot()
        plt.axis('square')
        plt.draw()
        plt.pause(0.001)
