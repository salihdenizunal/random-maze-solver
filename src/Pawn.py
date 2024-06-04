from PathFinder import PathFinder
from Maze import Maze
import matplotlib.pyplot as plt

class Pawn:
    """
    The Pawn class represents a pawn object in a maze.

    Attributes:
    - position (tuple): The current position of the pawn.
    - goal (tuple): The goal position of the pawn.
    - maze (Maze): The maze object representing the maze.
    - __path (list): The path of the pawn as a list of indices.
    - move_history (list): The history of the pawn's moves as a list of positions.
    - __pathFinder (PathFinder): The path finder object used to find the shortest path.

    Methods:
    - __init__(startPosition, goal, maze): Initializes the Pawn object.
    - setGoal(goal): Sets the goal position of the pawn.
    - getGoal(): Returns the goal position of the pawn.
    - setPath(path): Sets the path of the pawn.
    - getPath(): Returns the path of the pawn.
    - setMaze(maze): Sets the maze object for the pawn.
    - move(): Moves the pawn to the next position in the path.
    - plot(): Plots the pawn's path on a graph.
    - findPath(): Finds the shortest path from the start position to the goal position.
    """

    def __init__(self, startPosition : tuple, goal : tuple, maze : Maze):
        """
        Initialize the Pawn object.

        Parameters:
        - startPosition: The starting position of the pawn.
        - goal: The goal position of the pawn.
        - maze: The maze object representing the maze.

        Returns:
        None
        """
        self.position = startPosition
        self.goal = goal
        self.setMaze(maze)
        self.setPath([])
        self.move_history = [startPosition]
        self.__pathFinder = PathFinder(self.__maze.converToGraph(), self.position, self.goal)
    
    def setGoal(self, goal):
        """
        Set the goal position of the pawn.

        Parameters:
        - goal: The new goal position.

        Returns:
        None
        """
        self.goal = goal

    def getGoal(self):
        """
        Get the goal position of the pawn.

        Parameters:
        None

        Returns:
        The goal position.
        """
        return self.goal
    
    def setPath(self, path : list):
        """
        Set the path of the pawn.

        Parameters:
        - path: The new path as a list of indices.

        Returns:
        None
        """
        self.__path = path
    
    def getPath(self):
        """
        Get the path of the pawn.

        Parameters:
        None

        Returns:
        The path as a list of indices.
        """
        return self.__path
    
    def setMaze(self, maze : Maze):
        """
        Set the maze object for the pawn.

        Parameters:
        - maze: The maze object.

        Returns:
        None
        """
        self.__maze = maze
    
    def move(self):
        """
        Move the pawn to the next position in the path.

        Parameters:
        None

        Returns:
        None
        """
        if self.position != self.goal and len(self.__path) > 0:
            nextIndex = self.__path[self.__path.index(self.__maze.findIndexOfVertex(self.position)) + 1]
            self.position = self.__maze.vertices[nextIndex]

            # Remove the previous position from the path
            self.__path = self.__path[1:]

            # Add the current position to the move history.
            self.move_history.append(self.position)

    def plot(self):
        """
        Plot the pawn's path on a graph.

        Parameters:
        None

        Returns:
        None
        """
        # Plot the path if available.
        if self.__path:
            pathCoords = [self.__maze.vertices[i] for i in self.__path]
            path_x = [coord[0] for coord in pathCoords]
            path_y = [coord[1] for coord in pathCoords]
            plt.plot(path_x, path_y, 'b', linewidth=2)

        # Plot the move history if available.
        if self.move_history:
            move_x = [coord[0] for coord in self.move_history]
            move_y = [coord[1] for coord in self.move_history]
            plt.plot(move_x, move_y, 'lightblue', linewidth=1)

            # Plot start flag.
            plt.plot(move_x[0], move_y[0], 'ro', color='lightblue', markersize=8)

        # Plot start marker.
        plt.plot(self.position[0], self.position[1], 'go', markersize=10)

        # Plot finish flag.
        flag_x = self.goal[0] + 0.17
        flag_y = self.goal[1] + 0.73
        plt.plot(flag_x, flag_y, marker='>', color='r', markersize=12)
        
        # Plot flagpole.
        plt.plot([self.goal[0], self.goal[0]], [self.goal[1] + 0.5, self.goal[1] ], color='black', linewidth=3)
        
        # Plot flagpole base.
        plt.plot([self.goal[0] - 0.1, self.goal[0] + 0.1], [self.goal[1], self.goal[1]], color='black', linewidth=3)
        
    
    def findPath(self):
        """
        Find the shortest path from the start position to the goal position.

        Parameters:
        None

        Returns:
        The shortest path as a list of indices, or None if no valid path is found.
        """
        # Set the graph, start position, and goal position for the path finder.
        self.__pathFinder.setGraph(self.__maze.converToGraph())
        self.__pathFinder.setStart(self.position)
        self.__pathFinder.setGoal(self.goal)
        
        # Get the A* path mapping from the path finder.
        aStarMap = self.__pathFinder.getPathMapping()
        
        # If no valid path is found, return None.
        if aStarMap is None: return None

        # Construct the shortest path from the A* path mapping.
        shortestPath = []
        indexOf_startVertex = self.__maze.findIndexOfVertex(self.position)
        indexOf_endVertex = self.__maze.findIndexOfVertex(self.goal)

        shortestPath.append(indexOf_endVertex)
        while indexOf_endVertex != indexOf_startVertex:
            temp = aStarMap[indexOf_endVertex]
            shortestPath.append(temp)
            indexOf_endVertex = temp
        shortestPath.reverse()

        # If the shortest path starts from the start vertex, return the path.
        if shortestPath[0] == indexOf_startVertex: return shortestPath
        # No valid path found.
        else: return None
