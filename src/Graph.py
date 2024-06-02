import numpy as np

class Graph:
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges
        
    # Check if the given vertex is a vertex of the given graph.
    def hasVertex(self, v):
        return any([v == vertex for vertex in self.vertices])
 
    # Find the index of the given vertex in the given graph.
    def findIndexOfVertex(self, v):
        for i, vertex in enumerate(self.vertices):
            if np.array_equal(vertex, v):
                return i
        return -1
    
    # Find the successors of the given vertex in the given graph.
    def getSuccessors(self, v):
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
    

