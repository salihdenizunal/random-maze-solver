import numpy as np
import math

# Check if the given vertex is a vertex of the given graph.
def isVertex(v, G):
    if isinstance(G, dict) and 'V' in G:
        return any([v == vertex for vertex in G['V']])
    return False

# Find the index of the given vertex in the given graph.
def findIndexOfVertex(v, G):
    for i, vertex in enumerate(G['V']):
        if np.array_equal(vertex, v):
            return i
    return -1

# Find the successors of the given vertex in the given graph.
def findSuccessors(v, G):
  assert(isVertex(v, G))
  index = findIndexOfVertex(v, G)
  successors = []
  for edge in G['E']:
    # If first vertex of the edge is the given vertex, the second vertex is successor.
    # And vice versa.
    if edge[0] == index:
      successors.append(G['V'][edge[1]])
    elif edge[1] == index:
      successors.append(G['V'][edge[0]])
  return np.array(successors)

# Heuristic measure takes the distance between two given vertices.
def heuristicMeasure(v1, v2):
  return math.sqrt(pow((v1[0] - v2[0]), 2) + pow((v1[1] - v2[1]), 2))

def A_star(G, s, r):
  assert(isVertex(s, G) and isVertex(r, G))

  # pi -> mapping
  pi = {}
  # S  -> open list
  S = set()
  # g  -> cost function
  g = {}
  # h  -> heuristic lower bound estimate
  h = {}

  # Find the index of vertices.
  indexOf_s = findIndexOfVertex(s, G)
  indexOf_r = findIndexOfVertex(r, G)

  # Initialization.
  for v in G['V']:
    indexOf_v = findIndexOfVertex(v, G)
    g[(indexOf_s, indexOf_v)] = math.inf
    pi[indexOf_v] = None

  g[(indexOf_s, indexOf_s)] = 0
  S.add(indexOf_s)
  h[(indexOf_s, indexOf_r)] = heuristicMeasure(s, r)

  # Search.
  while len(S) > 0:
    # Vertex vPrime € S that minimizes g(s->vPrime) + h(vPrime -> r)
    minEstimation = math.inf
    v = None
    for indexOf_vPrime in S:
      minEstimationPrime = g[(indexOf_s, indexOf_vPrime)] + h[(indexOf_vPrime, indexOf_r)]
      if minEstimationPrime <= minEstimation:
        v = G['V'][indexOf_vPrime]
        minEstimation = minEstimationPrime

    # Is the goal reached?
    indexOf_v = findIndexOfVertex(v, G)
    if indexOf_v == indexOf_r:
      return pi

    S.remove(indexOf_v)

    # Open u.
    for u in findSuccessors(v, G):
      indexOf_u = findIndexOfVertex(u, G)
      if (pi[indexOf_u] == None) or (indexOf_u in S and (g[(indexOf_s, indexOf_v)] + heuristicMeasure(v, u) < g[(indexOf_s,indexOf_u)])):
        S.add(indexOf_u)
        g[(indexOf_s, indexOf_u)] = g[(indexOf_s, indexOf_v)] + heuristicMeasure(v, u)
        pi[indexOf_u] = indexOf_v
        h[(indexOf_u, indexOf_r)] =  heuristicMeasure(u, r)

  return None