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

    def __init__(self, rows=15, cols=15):
        """
        Initialize the DynamicMaze object.

        Parameters:
        - rows: The number of rows in the maze. Default is 15.
        - cols: The number of columns in the maze. Default is 15.

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

        # Generate a random starting value for the lcg2 function call
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
        # If a vertex has only one neighbor (including the other end of the wall being added),
        # adding this wall would isolate it, which is undesirable. In this case, the method 
        # returns True, indicating that adding this wall would create a chain.
        if len(startNeighbors) == 1 or len(endNeighbors) == 1:
            return True

        # Verify if the start and end vertices are already connected by other walls.
        # If they are, then adding this wall won't create a chain. The method checks
        # if any neighbor of the start vertex is the same as any neighbor of the end vertex.
        # If such a neighbor exists, it means the start and end vertices are already connected,
        # and hence adding this wall won't create a chain.
        startConnected = any(neigh in startNeighbors for neigh in endNeighbors)
        if startConnected:
            return False  # Adding this wall won't create a chain

        # If the start and end vertices are not already connected, the method examines
        # if adding this wall would create a chain for the start vertex. It checks if all
        # neighbors of the start vertex already have walls between them and the start vertex.
        # If so, adding this wall would isolate the start vertex from the rest of the maze,
        # creating a chain.
        startChain = all(self.hasWall((start, neigh)) for neigh in startNeighbors)
        if startChain:
            return True  # Adding this wall will create a chain

        # Similarly, if adding the wall wouldn't create a chain at the start vertex,
        # it checks if it would create a chain at the end vertex. It examines if
        # all neighbors of the end vertex already have walls between them and the end vertex.
        # If so, adding this wall would isolate the end vertex from the rest of the maze,
        # creating a chain.
        endChain = all(self.hasWall((end, neigh)) for neigh in endNeighbors)
        if endChain:
            return True  # Adding this wall will create a chain

        return False  # Adding this wall won't create a chain

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
            # Add or remove walls        
            row = (self.randomNumberGenerator.generate() % (self.getRows() - 1))
            col = (self.randomNumberGenerator.generate() % (self.getCols() - 1))

            start = (row, col)
            # Randomly select the direction of the end vertex (up, down, left, right)
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            direction = directions[self.randomNumberGenerator.generate() % 4]

            end = (start[0] + direction[0], start[1] + direction[1])
            wall = (start, end)
            if self.hasWall(wall):
                self.__removeWall(wall)  # Remove wall

                self.pawn.setMaze(self.copy())
                calculatedPath = self.pawn.findPath()
                self.pawn.setPath(calculatedPath)
            else:
                if self.__createsChain(wall):
                    continue
                self.__addWall(wall)  # Add wall

                self.pawn.setMaze(self.copy())
                calculatedPath = self.pawn.findPath()
                if calculatedPath is None:
                    self.__removeWall(wall)
                    self.pawn.setMaze(self.copy())
                else:
                    self.pawn.setPath(calculatedPath)

    def plot(self):
        """
        Plot the maze and the pawn.

        Returns:
        None
        """
        # Plot the maze and the pawn
        plt.clf()
        super().plot()
        self.pawn.plot()
        # Set plot properties
        plt.axis('square')
        plt.draw()
        plt.pause(0.001)  # Add a small pause to allow for plot updates
