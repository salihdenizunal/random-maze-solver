from Graph import Graph
import numpy as np

import matplotlib.pyplot as plt

class Maze:
    """
    Represents a maze and provides functionalities to manipulate and visualize it.
    """

    def __init__(self, rows=12, cols=12):
        """
        Initializes a new instance of the Maze class.

        Args:
            rows (int): The number of rows in the maze.
            cols (int): The number of columns in the maze.
        """
        self.__rows = rows
        self.__cols = cols
        self.vertices = []
        self.walls = []
        self.__initMaze()

    def getRows(self):
        """
        Returns the number of rows in the maze.

        Returns:
            int: The number of rows in the maze.
        """
        return self.__rows

    def getCols(self):
        """
        Returns the number of columns in the maze.

        Returns:
            int: The number of columns in the maze.
        """
        return self.__cols

    def copy(self):
        """
        Creates a copy of the maze.

        Returns:
            Maze: A copy of the maze.
        """
        copyMaze = Maze(self.__rows, self.__cols)
        copyMaze.vertices = self.vertices
        copyMaze.walls = self.walls
        return copyMaze

    def __initMaze(self):
        """
        Initializes the maze by creating vertices and walls.
        """
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
        """
        Returns the north neighbor of a vertex.

        Args:
            xind (int): The x-coordinate of the vertex.
            yind (int): The y-coordinate of the vertex.

        Returns:
            tuple: The coordinates of the north neighbor.
        """
        node = (xind, yind + 1)
        return node

    def __east(self, xind, yind):
        """
        Returns the east neighbor of a vertex.

        Args:
            xind (int): The x-coordinate of the vertex.
            yind (int): The y-coordinate of the vertex.

        Returns:
            tuple: The coordinates of the east neighbor.
        """
        node = (xind + 1, yind)
        return node

    def isVertex(self, node):
        """
        Checks if a node is a valid vertex in the maze.

        Args:
            node (tuple): The coordinates of the node.

        Returns:
            bool: True if the node is a vertex, False otherwise.
        """
        return node in self.vertices

    def hasWall(self, wall):
        """
        Checks if a wall exists in the maze.

        Args:
            wall (tuple): The wall to check.

        Returns:
            bool: True if the wall exists, False otherwise.
        """
        return wall in self.walls

    def findIndexOfVertex(self, v):
        """
        Finds the index of a vertex in the maze.

        Args:
            v (tuple): The coordinates of the vertex.

        Returns:
            int: The index of the vertex, or -1 if not found.
        """
        for i, vertex in enumerate(self.vertices):
            if np.array_equal(vertex, v):
                return i
        return -1

    def getNeighborVertices(self, vertex):
        """
        Returns the indices of the neighboring vertices of a given vertex.

        Args:
            vertex (tuple): The coordinates of the vertex.

        Returns:
            list: The indices of the neighboring vertices.
        """
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
        """
        Converts the maze to a graph representation.

        Returns:
            Graph: The graph representation of the maze.
        """
        edges = []
        for vertex in self.vertices:
            for neighbor_id in self.getNeighborVertices(vertex):
                edges.append((self.findIndexOfVertex(vertex), neighbor_id))

        graph = Graph(self.vertices, edges)
        return graph

    def plot(self, vertexFlag=False):
        """
        Plots the maze.

        Args:
            vertexFlag (bool): Whether to plot the vertices of the maze.
        """
        # Plot the walls of the maze
        for e in self.walls:
            vec = np.array([e[1][0] - e[0][0], e[1][1] - e[0][1]])
            ort = np.array([-vec[1], vec[0]])
            olen = np.linalg.norm(ort)
            ort = ort / olen
            sum = np.array([(e[1][0] + e[0][0]) / 2, (e[1][1] + e[0][1]) / 2])
            startp = sum - ort / 2
            endp = sum + ort / 2
            plt.plot((startp[0], endp[0]), (startp[1], endp[1]), 'gray', linewidth=10)

        # Plot the vertices of the maze if vertexFlag is True
        if vertexFlag:
            for v in self.vertices:
                plt.plot(float(v[0]), float(v[1]), 'ro')