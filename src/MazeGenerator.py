from RandomNumberGenerator import RandomNumberGenerator
from Maze import Maze

class MazeGenerator:
    """
    This class represents a maze generator.

    Attributes:
        maze (Maze): The maze object.
        __randomNumberGenerator (RandomNumberGenerator): The random number generator object.

    Methods:
        __init__(self, rows=12, cols=12): Initializes a MazeGenerator object.
        __randomItem(self, fromList): Returns a random item from a given list.
        generateMaze(self): Generates a maze using the randomized Prim's algorithm.
    """

    def __init__(self, rows=12, cols=12):
        """
        Initializes a MazeGenerator object.

        Args:
            rows (int): The number of rows in the maze. Default is 12.
            cols (int): The number of columns in the maze. Default is 12.
        """
        self.maze = Maze(rows, cols)
        self.__randomNumberGenerator = RandomNumberGenerator()

    def __randomItem(self, fromList):
        """
        Returns a random item from a given list.

        Args:
            fromList (list): The list to choose from.

        Returns:
            object: A random item from the list.
        """
        randind = (self.__randomNumberGenerator.generate() % len(list(fromList)))
        return list(fromList)[randind]

    def generateMaze(self):
        """
        Generates a maze using the randomized Prim's algorithm.

        Returns:
            Maze: The generated maze.
        """
        assert(type(self.maze == Maze)), "The self maze should be type Maze."

        # Visited cells C from Vertexes of G.
        # All cells are unvisited.
        C = set()

        # All connections have walls.
        W = self.maze.walls.copy()

        # Set of walls to check out L.
        L = set()

        # Select c € V randomly.
        c = self.__randomItem(self.maze.vertices)

        # Initialize L with the neighbours of c.
        for w in W:
            if c in w:
                L.add(w)

        while L:
            # Select l € L randomly.
            l = self.__randomItem(L)

            if not l in C:
                # Both ends not already visited.
                if(len(set(l).intersection(C)) <= 1):
                    for endPt in l:
                        C.add(endPt)

                    # Remove the wall.
                    W.remove(l)

                    # Add neighbouring walls.
                    for w in W:
                        if len(set(w).intersection(l)) != 0:
                            if not w in L:
                                L.add(w)
            L.remove(l)

        self.maze.walls = W
        return self.maze
