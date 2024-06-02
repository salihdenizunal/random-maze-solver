import math
from Graph import Graph

class PathFinder:
    def __init__(self, graph : Graph, start, goal):
        self.start = start
        self.goal = goal
        self.setGraph(graph)
    
    def setStart(self, start):
        self.start = start
        
    def setGoal(self, goal):
        self.goal = goal
           
    def setGraph(self, graph : Graph):
        self.graph = graph
    
    # Heuristic measure takes the distance between two given vertices.
    def __heuristicMeasure(self, v1, v2):
        return math.sqrt(pow((v1[0] - v2[0]), 2) + pow((v1[1] - v2[1]), 2))
    
    def getPathMapping(self):
        assert(self.graph.isVertex(self.start) and self.graph.isVertex(self.goal))

        # pi -> mapping
        pi = {}
        # S  -> open list
        S = set()
        # g  -> cost function
        g = {}
        # h  -> heuristic lower bound estimate
        h = {}

        # Find the index of vertices.
        indexOf_s = self.graph.findIndexOfVertex(self.start)
        indexOf_r = self.graph.findIndexOfVertex(self.goal)

        # Initialization.
        for v in self.graph.vertices:
            indexOf_v = self.graph.findIndexOfVertex(v)
            g[(indexOf_s, indexOf_v)] = math.inf
            pi[indexOf_v] = None

        g[(indexOf_s, indexOf_s)] = 0
        S.add(indexOf_s)
        h[(indexOf_s, indexOf_r)] = self.__heuristicMeasure(self.start, self.goal)

        # Search.
        while len(S) > 0:
            # Vertex vPrime € S that minimizes g(s->vPrime) + h(vPrime -> r)
            minEstimation = math.inf
            v = None
            for indexOf_vPrime in S:
                minEstimationPrime = g[(indexOf_s, indexOf_vPrime)] + h[(indexOf_vPrime, indexOf_r)]
                if minEstimationPrime <= minEstimation:
                    v = self.graph.vertices[indexOf_vPrime]
                    minEstimation = minEstimationPrime

            # Is the goal reached?
            indexOf_v = self.graph.findIndexOfVertex(v)
            if indexOf_v == indexOf_r:
                return pi

            S.remove(indexOf_v)

            # Open u.
            for u in self.graph.findSuccessors(v):
                indexOf_u = self.graph.findIndexOfVertex(u)
                if (pi[indexOf_u] == None) or (indexOf_u in S and (g[(indexOf_s, indexOf_v)] + self.__heuristicMeasure(v, u) < g[(indexOf_s,indexOf_u)])):
                    S.add(indexOf_u)
                    g[(indexOf_s, indexOf_u)] = g[(indexOf_s, indexOf_v)] + self.__heuristicMeasure(v, u)
                    pi[indexOf_u] = indexOf_v
                    h[(indexOf_u, indexOf_r)] = self.__heuristicMeasure(u, self.goal)

        return None