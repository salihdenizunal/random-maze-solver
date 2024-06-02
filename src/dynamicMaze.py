from MazeGenerator import MazeGenerator
from Pawn import Pawn
from Maze import Maze
from RandomNumberGenerator import RandomNumberGenerator
import random
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
        
    def remove_wall(self, wall):
        if self.has_wall(wall):
            self.walls.remove(wall)

    def add_wall(self, wall):
        if not self.has_wall(wall):
            self.walls.append(wall)

    def plot(self):
        plt.clf()
        super().plot()
        self.pawn.plot()
        # Set plot properties
        plt.axis('square')
        plt.draw()
        plt.pause(0.001)  # Add a small pause to allow for plot updates
        
    def updateMaze(self):
        # Add or remove walls
        row = random.randint(0, self.rows - 1)
        col = random.randint(0, self.cols - 1)

        buffer = min(self.rows, self.cols)

        start = (row, col)
        # Randomly select the direction of the end vertex (up, down, left, right)
        direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        end = (start[0] + direction[0], start[1] + direction[1])
        wall = (start, end)
        if self.has_wall(wall):
            if len(self.walls) + buffer < len(self.vertices):
                return
            self.remove_wall(wall)  # Remove wall

            calculatedPath = self.pawn.findPath()
            if calculatedPath is None:
                self.add_wall(wall)
            else:
                self.pawn.setPath(calculatedPath)
                self.pawn.setMaze(self.copy())
        else:
            if len(self.walls) - buffer > len(self.vertices) :
                return
            self.add_wall(wall)  # Add wall

            calculatedPath = self.pawn.findPath()
            if calculatedPath is None:
                self.remove_wall(wall)
            else:
                self.pawn.setPath(calculatedPath)
                self.pawn.setMaze(self.copy())

