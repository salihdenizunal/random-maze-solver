import numpy as np

class Graph:
    """
    A class representing a graph.

    Attributes:
        vertices (list): List of vertices in the graph.
        edges (list): List of edges in the graph.

    Methods:
        hasVertex(v): Check if the given vertex is a vertex of the graph.
        findIndexOfVertex(v): Find the index of the given vertex in the graph.
        getSuccessors(v): Find the successors of the given vertex in the graph.
    """

    def __init__(self, vertices, edges):
        """
        Initialize a Graph object.

        Args:
            vertices (list): List of vertices in the graph.
            edges (list): List of edges in the graph.
        """
        self.vertices = vertices
        self.edges = edges
        
    def hasVertex(self, v):
        """
        Check if the given vertex is a vertex of the graph.

        Args:
            v: The vertex to check.

        Returns:
            bool: True if the vertex is in the graph, False otherwise.
        """
        return any([v == vertex for vertex in self.vertices])
 
    def findIndexOfVertex(self, v):
        """
        Find the index of the given vertex in the graph.

        Args:
            v: The vertex to find the index of.

        Returns:
            int: The index of the vertex in the graph, or -1 if not found.
        """
        for i, vertex in enumerate(self.vertices):
            if np.array_equal(vertex, v):
                return i
        return -1
    
    def getSuccessors(self, v):
        """
        Find the successors of the given vertex in the graph.

        Args:
            v: The vertex to find the successors of.

        Returns:
            numpy.ndarray: An array of successors of the vertex.
        """
        assert(self.hasVertex(v))
        index = self.findIndexOfVertex(v)
        successors = []
        for edge in self.edges:
            # If first vertex of the edge is the given vertex, the second vertex is successor.
            # And vice versa.
            if edge[0] == index:
                successors.append(self.vertices[edge[1]])
            elif edge[1] == index:
                successors.append(self.vertices[edge[0]])
        return np.array(successors)
