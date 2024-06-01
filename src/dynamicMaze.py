import mazeGenerator
import pathFinder
import random
import matplotlib.pyplot as plt
import numpy as np

class DynamicMaze:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        # Generate a random starting value for the lcg2 function call
        self.startingVal = 1
        self.pointer =  (0, 0)  # Initialize pointer at the start position
        self.maze = mazeGenerator.generateMaze(rows, cols, self.startingVal)
        self.end = (rows - 1, cols - 1)  # End position
        self.path = self.findPath()
    
    def plot(self, vertexFlag = False):
        # Clear the previous plot
        plt.clf()
        
        # Plot the walls of the maze
        for e in self.maze['W']:
            vec = np.array([e[1][0]-e[0][0], e[1][1]-e[0][1]])
            ort = np.array([-vec[1], vec[0]])
            olen = np.linalg.norm(ort)
            ort = ort / olen
            sum = np.array([(e[1][0]+e[0][0])/2, (e[1][1]+e[0][1])/2])
            startp = sum - ort / 2
            endp = sum + ort / 2
            plt.plot((startp[0], endp[0]), (startp[1], endp[1]), 'gray', linewidth=10)
        
        # Plot the vertices of the maze if vertexFlag is True
        if vertexFlag:
            for v in self.maze['V']:
                plt.plot(float(v[0]), float(v[1]), 'ro')
        
        # Plot the path if provided
        if self.path:
            path_coords = [self.maze['V'][i] for i in self.path]
            path_x = [coord[0] for coord in path_coords]
            path_y = [coord[1] for coord in path_coords]
            plt.plot(path_x, path_y, 'b', linewidth=2)

        # Plot start marker 
        start_coords = self.maze['V'][self.path[0]]
        plt.plot(start_coords[0], start_coords[1], 'go', markersize=10)

        # Plot finish flag
        end_coords = self.maze['V'][self.path[-1]]
        flag_x = end_coords[0] + 0.2
        flag_y = end_coords[1] + 0.7  # Adjust the flag height
        plt.plot([end_coords[0], end_coords[0]], [end_coords[1] + 0.5, end_coords[1] ], color='black', linewidth=3)  # Plot flagpole
        plt.plot(flag_x, flag_y, marker='>', color='r', markersize=12)  # Plot flag with triangle facing right

        # Set plot properties
        plt.axis('square')
        plt.draw()
        plt.pause(0.001)  # Add a small pause to allow for plot updates


    def move(self):
        if self.pointer != self.end:
            next_index = self.path[self.path.index(self.findIndexOfVertex(self.pointer)) + 1]
            self.pointer = self.maze['V'][next_index]

    def has_wall(self, wall):
        return wall in self.maze['W']

    def remove_wall(self, wall):
        if self.has_wall(wall):
            self.maze['W'].remove(wall)

    def add_wall(self, wall):
        if not self.has_wall(wall):
            self.maze['W'].append(wall)

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
            if len(self.maze['W']) + buffer < len(self.maze['V']):
                return
            self.remove_wall(wall)  # Remove wall

            calculatedPath = self.findPath()
            if calculatedPath is None:
                self.add_wall(wall)
            else:
                self.path = calculatedPath
        else:
            if len(self.maze['W']) - buffer > len(self.maze['V']) :
                return
            self.add_wall(wall)  # Add wall

            calculatedPath = self.findPath()
            if calculatedPath is None:
                self.remove_wall(wall)
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
            if (vertex, neighbor) in self.maze['W'] or (neighbor, vertex) in self.maze['W']:
                continue
            if self.isVertex(neighbor):
                adjacent_vertices.append(self.findIndexOfVertex(neighbor))
        return adjacent_vertices

    def construct_graph(self):
        # Add vertices from the maze
        graph = {'V': [], 'E': []}
        graph['V'] = self.maze['V']

        # Create walls between adjacent vertices (excluding walls)
        for vertex in self.maze['V']:
            for neighbor_id in self.get_adjacent_vertices(vertex):
                graph['E'].append((self.findIndexOfVertex(vertex), neighbor_id))
        return graph

    def findPath(self):
        aStarMap = pathFinder.A_star(self.construct_graph(), self.pointer, self.end)
        if aStarMap is None:
            return None

        shortestPath = []
        indexOf_startVertex = self.findIndexOfVertex(self.pointer)
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