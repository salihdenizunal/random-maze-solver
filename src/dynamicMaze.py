import mazeGenerator
import pathFinder
import randomNumberGenerator
import random
import numpy as np

class DynamicMaze:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        # Generate a random starting value for the lcg2 function call
        self.startingVal = 1
        self.maze = mazeGenerator.generateMaze(rows, cols, self.startingVal)
        self.start = (0, 0)  # Start position
        self.end = (rows - 1, cols - 1)  # End position
        self.path = self.findPath()

    def has_edge(self, edge):
        return edge in self.maze['E']

    def remove_edge(self, edge):
        if self.has_edge(edge):
            self.maze['E'].remove(edge)

    def add_edge(self, edge):
        if not self.has_edge(edge):
            self.maze['E'].append(edge)

    def updateMaze(self, updateFactor = 10):
        random_val = randomNumberGenerator.lcg2(startingval=self.startingVal)  # Pass a new random starting value
        self.startingVal = random_val
        self.maze = mazeGenerator.generateMaze(self.rows, self.cols, randomNumber=self.startingVal)
        self.path = self.findPath()
        return
        for _ in range(int((self.rows*self.cols)/updateFactor)):
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

                    calculatedPath = self.findPath()
                    if calculatedPath is None:
                        self.add_edge(edge)
                    else:
                        self.path = calculatedPath
                else:
                    self.add_edge(edge)  # Add wall

                    calculatedPath = self.findPath()
                    if calculatedPath is None:
                        self.remove_edge(edge)
                    else:
                        self.path = calculatedPath

    def findIndexOfVertex(self, v):
        for i, vertex in enumerate(self.maze['V']):
            if np.array_equal(vertex, v):
                return i
        return -1
    
    def isVertex(self, v):
        if isinstance(self.maze, dict) and 'V' in self.maze:
            return any([v == vertex for vertex in self.maze['V']])
        return False

    def get_adjacent_vertices(self, vertex):
        i, j = vertex
        rows, cols = len(self.maze['V']), len(self.maze['V'][0])
        adjacent_vertices = []
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            x, y = i + dx, j + dy
            neighbor = (x, y)
            if (vertex, neighbor) in self.maze['E'] or (neighbor, vertex) in self.maze['E']:
                continue
            if self.isVertex(neighbor):
                adjacent_vertices.append(self.findIndexOfVertex(neighbor))
        return adjacent_vertices

    def construct_graph(self):
        # Add vertices from the maze
        graph = {'V': [], 'E': []}
        graph['V'] = self.maze['V']

        # Create edges between adjacent vertices (excluding walls)
        for vertex in self.maze['V']:
            for neighbor_id in self.get_adjacent_vertices(vertex):
                graph['E'].append((self.findIndexOfVertex(vertex), neighbor_id))
        return graph

    def findPath(self):
        aStarMap = pathFinder.A_star(self.construct_graph(), self.start, self.end)
        if aStarMap is None:
            return None

        shortestPath = []
        indexOf_startVertex = self.findIndexOfVertex(self.start)
        indexOf_endVertex = self.findIndexOfVertex(self.end)

        shortestPath.append(indexOf_endVertex)
        while indexOf_endVertex != indexOf_startVertex:
            temp = aStarMap[indexOf_endVertex]
            shortestPath.append(temp)
            indexOf_endVertex = temp
        shortestPath.reverse()

        if shortestPath[0] == indexOf_startVertex:
            return shortestPath
        else:
            return None  # No valid path found