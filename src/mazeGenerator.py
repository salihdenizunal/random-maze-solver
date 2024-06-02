from RandomNumberGenerator import RandomNumberGenerator
from Maze import Maze

class MazeGenerator:
    def __init__(self, rows = 15, cols = 15):
        self.maze = Maze(rows, cols)
        self.randomNumberGenerator = RandomNumberGenerator()

    def randomItem(self, fromList):
        randind = (self.randomNumberGenerator.generate() % len(list(fromList)))
        return list(fromList)[randind]

    # Returns the walls W from the walls of G that builds up a maze.
    def generateMaze(self):
        assert(type(self.maze == Maze)), "The self maze should be type Maze."

        # Visited cells C from Vertexes of G.
        # All cells are unvisited.
        C = set()

        # All connections have walls.
        W = self.maze.walls.copy()

        # Set of walls to check out L.
        L = set()

        # Select c € V randomly.
        c = self.randomItem(self.maze.vertices)

        # Initialize L with the neighbours of c.
        for w in W:
            if c in w:
                L.add(w)

        while L:
            # Select l € L randomly.
            l = self.randomItem(L)

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
