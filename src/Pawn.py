from PathFinder import PathFinder
from Maze import Maze
import matplotlib.pyplot as plt

class Pawn:
    def __init__(self, startPosition, goal, maze : Maze):
        self.position = startPosition
        self.goal = goal
        self.setMaze(maze)
        self.setPath([])
        self.__pathFinder = PathFinder(self.__maze.converToGraph(), self.position, self.goal)
        
    def setPath(self, path : list):
        self.__path = path
    
    def setMaze(self, maze : Maze):
        self.__maze = maze
    
    def move(self):
        if self.position != self.goal and len(self.__path) > 0:
            nextIndex = self.__path[self.__path.index(self.__maze.findIndexOfVertex(self.position)) + 1]
            self.position = self.__maze.vertices[nextIndex]

    def plot(self):
         # Plot the path if provided
        if self.__path:
            pathCoords = [self.__maze.vertices[i] for i in self.__path]
            path_x = [coord[0] for coord in pathCoords]
            path_y = [coord[1] for coord in pathCoords]
            plt.plot(path_x, path_y, 'b', linewidth=2)

        # Plot start marker 
        plt.plot(self.position[0], self.position[1], 'go', markersize=10)

        # Plot finish flag
        flag_x = self.goal[0] + 0.2
        flag_y = self.goal[1] + 0.7  # Adjust the flag height
        plt.plot([self.goal[0], self.goal[0]], [self.goal[1] + 0.5, self.goal[1] ], color='black', linewidth=3)  # Plot flagpole
        plt.plot(flag_x, flag_y, marker='>', color='r', markersize=12)  # Plot flag with triangle facing right
        
    
    def findPath(self):
        self.__pathFinder.setGraph(self.__maze.converToGraph())
        self.__pathFinder.setStart(self.position)
        self.__pathFinder.setGoal(self.goal)
        aStarMap = self.__pathFinder.getPathMapping()
        if aStarMap is None:
            return None

        shortestPath = []
        indexOf_startVertex = self.__maze.findIndexOfVertex(self.position)
        indexOf_endVertex = self.__maze.findIndexOfVertex(self.goal)

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