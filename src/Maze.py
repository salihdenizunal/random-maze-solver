from Graph import Graph
import numpy as np
import matplotlib.pyplot as plt

# To encapsulate the maze representation and related functionalities more effectively,
# the MazeGenerator class should contain a Maze class. This way, the Maze class can 
# handle the maze's internal structure and operations, allowing the MazeGenerator to 
# focus solely on generating the maze.
class Maze:
    def __init__(self, rows = 15, cols = 15):
        self.__rows = rows
        self.__cols = cols
        self.vertices = []
        self.walls = []
        self.__initMaze()
        
    def getRows(self):
        return self.__rows
    
    def getCols(self):
        return self.__cols
    
    def copy(self):
        copyMaze = Maze(self.__rows, self.__cols)
        copyMaze.vertices = self.vertices
        copyMaze.walls = self.walls
        return copyMaze

    def __initMaze(self):
        for xind in range(self.__rows):
            for yind in range(self.__cols):
                self.vertices.append((xind, yind))

        # Traverse north first
        for pt in self.vertices:
            vtn = self.__north(pt[0], pt[1])
            if self.isVertex(vtn):
                self.walls.append((pt, vtn))

        # Traverse east second
        for pt in self.vertices:
            vte = self.__east(pt[0], pt[1])
            if self.isVertex(vte):
                self.walls.append((pt, vte))

    def __north(self, xind, yind):
        node = (xind, yind + 1)
        return node

    def __east(self, xind, yind):
        node = (xind + 1, yind)
        return node

    def isVertex(self, node):
        return node in self.vertices
    
    def hasWall(self, wall):
        return wall in self.walls
    
    def findIndexOfVertex(self, v):
        for i, vertex in enumerate(self.vertices):
            if np.array_equal(vertex, v):
                return i
        return -1

    def getNeighborVertices(self, vertex):
        i, j = vertex
        neighborVertices = []
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            x, y = i + dx, j + dy
            neighbor = (x, y)
            if (vertex, neighbor) in self.walls or (neighbor, vertex) in self.walls:
                continue
            if self.isVertex(neighbor):
                neighborVertices.append(self.findIndexOfVertex(neighbor))
        return neighborVertices

    def converToGraph(self):
        # Create walls between adjacent vertices (excluding walls)
        edges = []
        for vertex in self.vertices:
            for neighbor_id in self.getNeighborVertices(vertex):
                edges.append((self.findIndexOfVertex(vertex), neighbor_id))
        
        graph = Graph(self.vertices, edges)
        return graph
    
    def plot(self, vertexFlag = False):       
        # Plot the walls of the maze
        for e in self.walls:
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
            for v in self.vertices:
                plt.plot(float(v[0]), float(v[1]), 'ro')
       