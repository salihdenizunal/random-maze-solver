import mazeGenerator
import pathFinder
import randomNumberGenerator
import random

class DynamicMaze:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        # Generate a random starting value for the lcg2 function call
        self.startingVal = 1
        self.maze = mazeGenerator.generateMaze(rows, cols)
        self.start = (0, 0)  # Start position
        self.end = (rows - 1, cols - 1)  # End position

    def has_edge(self, edge):
        return edge in self.maze['E']

    def remove_edge(self, edge):
        if self.has_edge(edge):
            self.maze['E'].remove(edge)

    def add_edge(self, edge):
        if not self.has_edge(edge):
            self.maze['E'].append(edge)

    def updateMaze(self, updateFactor=1):
        for _ in range(updateFactor):
            # Generate random number to decide whether to add or remove walls
            random_val = randomNumberGenerator.lcg2(startingval=self.startingVal)  # Pass a new random starting value
            self.startingVal = random_val
            if random_val % 2 == 0:
                # Add or remove walls
                row = random.randint(0, self.rows - 1)
                col = random.randint(0, self.cols - 1)
                start = (row, col)
                # Randomly select the direction of the end vertex (up, down, left, right)
                direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
                end = (start[0] + direction[0], start[1] + direction[1])
                edge = (start, end)
                if self.has_edge(edge):
                    self.remove_edge(edge)  # Remove wall
                else:
                    self.add_edge(edge)  # Add wall

    def findPath(self):
        return pathFinder.A_star(self.maze, self.start, self.end)
