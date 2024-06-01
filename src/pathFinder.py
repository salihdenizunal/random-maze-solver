import numpy as np
import matplotlib.pyplot as plt
import math
import random
from datetime import datetime

def seidel_trig(points):
    def orientation(p1, p2, p3):
        """Compute the orientation of the triplet (p1, p2, p3)
        Returns:
            >0 if the triplet is counter-clockwise
            =0 if the triplet is collinear
            <0 if the triplet is clockwise
        """
        # Define three vectors
        p1p = np.array([p1[0], p1[1], 0.])
        p2p = np.array([p2[0], p2[1], 0.])
        p3p = np.array([p3[0], p3[1], 0.])
        # Define differences
        p12 = p2p - p1p
        p23 = p3p - p2p
        # Take the cross product
        cv = np.cross(p12, p23)
        return cv[2]

    def is_ear(i, n, points):
        p1 = points[(i-1) % n]
        p2 = points[i % n]
        p3 = points[(i+1) % n]
        if orientation(p1, p2, p3) <= 0:
            # The triangle is not counter-clockwise, so it's not an ear
            return False
        for j in range(n):
            if j == i % n or j == (i-1) % n or j == (i+1) % n:
                continue
            p = points[j]
            if (p[0] > min(p1[0], p2[0]) and p[0] < max(p1[0], p2[0]) and
                    p[1] > min(p1[1], p2[1]) and p[1] < max(p1[1], p2[1])):
                # The point is inside the triangle, so it's not an ear
                return False
        return True

    n = len(points)
    triangulation = []
    edges = set()
    edgepoly = set()
    vertices = points

    for ind in range(n-1):
      e = (ind, ind+1)
      edgepoly = edgepoly.union({e})
      edgepoly = edgepoly.union({(n-1,0)})

    while n > 3:
      for i in range(n):
          if is_ear(i, n, points):
              #triangulation.append(((i-1) % n, i % n, (i+1) % n))
              triangulation.append((points[(i-1) % n,:], points[i % n,:], points[(i+1) % n,:]))
              ind1 = np.where((vertices == points[(i-1) % n,:]).all(axis=1))[0][0]
              ind2 = np.where((vertices == points[i % n,:]).all(axis=1))[0][0]
              ind3 = np.where((vertices == points[(i+1) % n,:]).all(axis=1))[0][0]
              # e1 = (ind1, ind2)
              # e2 = (ind2, ind3)
              e = (ind3, ind1)
              edges = edges.union({e})
              points = np.delete(points, i, 0)
              n -= 1
              break

    triangulation.append((points[0], points[1], points[2]))
    ind1 = np.where((vertices == points[0,:]).all(axis=1))[0][0]
    ind2 = np.where((vertices == points[1,:]).all(axis=1))[0][0]
    ind3 = np.where((vertices == points[2,:]).all(axis=1))[0][0]
    # e1 = (ind1, ind2)
    # e2 = (ind2, ind3)
    e = (ind3, ind1)
    edges = edges.union({e})
    return triangulation, edges, vertices, edgepoly

def hertel_mehlhorn(poly_ccwpoints):
  trigs, edges, vertices, edgepoly = seidel_trig(simproom)
  n = len(vertices)
  edgeall = alledges(edges, edgepoly)

  for edge in edges:
    essflag = False
    vinds = edge # vertices to be checked. If essential for either one of these vertices
    for vind in vinds:
      ess = isessential(vertices, vind, edgeall, edge)
      essflag |= ess
    if not essflag:
      edges = edges.difference({edge})
      edges = edges.difference({(edge[1], edge[0])})
  return edges

def alledges(edgepoly, edges):
  return edgepoly.union(edges)

def isessential(vertices, vind, edgeall, edgetocheck):
  try:
    assert vind in edgetocheck
  except AssertionError:
    raise AssertionError('Edge not in vertex')

  if edgetocheck[1] == vind:
    edgetocheck = tuple(reversed(edgetocheck))

  if isvertexconvex(vertices, vind):
    return False

  n = len(vertices)

  egpol = edgesfromvertex(edgeall, vind) # All edges containing the polygon from the vertex
  egord = ccw_order(vertices, vind, egpol) # Triangulated edges ordered in CCW order
  sgn1 = orderedcross(vertices, egord)
  egord.remove(edgetocheck)
  sgn2 = orderedcross(vertices, egord)

  return sgn1 != sgn2

def isvertexconvex(vertices, vindex):
  n = len(vertices)
  p0 = vertices[vindex % n]
  p1 = vertices[(vindex - 1) % n]
  p2 = vertices[(vindex + 1) % n]
  vp = p2 - p0
  vn = p1 - p0
  vpp = np.array([vp[0], vp[1], 0.])
  vnp = np.array([vn[0], vn[1], 0.])
  return isconvex(vpp, vnp)

def edgesfromvertex(edges, vindex):
  vertexedges = []
  for edge in edges:
    if vindex in edge: # If either the start of end point for an edge
      if vindex == edge[1]:
        edge = (edge[1], edge[0])
      vertexedges.append(edge)
  return vertexedges

def isconvex(v1, v2):
  return np.cross(v1, v2)[2] > 0

def ccw_order(vertices, vind, edges):
  origin = [vertices[vind,0], vertices[vind,1]] # Assuming vectors are relative to the origin
  edges.sort(key=lambda e: math.atan2(vertices[e[1],1] - origin[1], vertices[e[1],0] - origin[0]))
  return edges

def orderedcross(vertices, edges):
  # Given a set of edges ordered in CCW order, removing an essential edge will change the sign of the
  # product of pairwise cross products
  m = len(edges)
  sgn = 1
  for eind in range(m):
    e1 = edges[eind % m]
    e2 = edges[(eind + 1) % m]
    v1 = vertices[e1[1], :]-vertices[e1[0], :]
    v2 = vertices[e2[1], :]-vertices[e2[0], :]
    v1p = np.array([v1[0], v1[1], 0.])
    v2p = np.array([v2[0], v2[1], 0.])
    sgnnew = np.sign(np.cross(v1p, v2p)[2])
    if sgnnew == 0: # np.sign(0) is zero so we map it as a non-convex i.e. pi angle
      sgnnew = -1
    sgn *= sgnnew
  return sgn


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
