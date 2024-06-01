import numpy as np

def undirectedconnectiongraph(xnum=30, ynum=30):
  G = {'V':[], 'E':[]} # We will use a dictionary for simplicity
  for xind in range(xnum):
    for yind in range(ynum):
      G['V'].append((xind, yind))

  # Traverse north first
  for pt in G['V']:
    vtn = north(pt[0], pt[1])
    if isvertex(vtn, G['V']):
      G['E'].append((pt, vtn))

  # Traverse east second
  for pt in G['V']:
    vte = east(pt[0], pt[1])
    if isvertex(vte, G['V']):
      G['E'].append((pt, vte))
  return G

def north(xind, yind):
  node = (xind, yind + 1)
  return node

def east(xind, yind):
  node = (xind + 1, yind)
  return node

def isvertex(node, vertices):
  return node in vertices

def randomnode(vertices):
  vertices = list(vertices)
  randind = np.random.randint(0, len(vertices))
  return vertices[randind]

# Returns the walls W from the Edges of G that builds up a maze.
def generateMaze(rows=20, cols=20):
  G = undirectedconnectiongraph(rows, cols)
  assert(type(G) == dict), "The undirected connection graph shall be a dictionary."
  assert('E' in G.keys()), "The undirected connection graph shall have a key as 'E' for the edges."
  assert('V' in G.keys()), "The undirected connection graph shall have a key as 'V' for the vertices."
  assert(len(G) == 2), "The undirected connection graph shall only have 2 keys."

  # Visited cells C from Vertexes of G.
  # All cells are unvisited.
  C = set()

  # All connections have walls.
  W = G['E'].copy()

  # Set of walls to check out L.
  L = set()

  # Select c € V randomly.
  c = randomnode(G['V'])

  # Initialize L with the neighbours of c.
  for w in W:
    if c in w:
      L.add(w)

  while L:
    # Select l € L randomly.
    l = randomnode(L)

    if not l in C:
      # Both ends not already visited.
      if(len(set(l).intersection(C)) <= 1):
        for endPt in l:
          C.add(endPt)

        # Remove the wall.
        W.remove(l)

        # Add neighbouring walls.
        for w in W:
          if len(set(w).intersection(l)) != 0:
            if not w in L:
              L.add(w)
    L.remove(l)

  return { 'V': G['V'], 'E': W }
