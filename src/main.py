import matplotlib.pyplot as plt
from dynamicMaze import DynamicMaze
import time
import numpy as np

# Function to plot the maze graph
def plotgraph(G, vertexflag=False):
    # Clear the previous plot
    plt.clf()
    
    # Plot the edges of the maze
    for e in G['E']:
        vec = np.array([e[1][0]-e[0][0], e[1][1]-e[0][1]])
        ort = np.array([-vec[1], vec[0]])
        olen = np.linalg.norm(ort)
        ort = ort / olen
        sum = np.array([(e[1][0]+e[0][0])/2, (e[1][1]+e[0][1])/2])
        startp = sum - ort / 2
        endp = sum + ort / 2
        plt.plot((startp[0], endp[0]), (startp[1], endp[1]), 'k', linewidth=10)
    
    # Plot the vertices of the maze if vertexflag is True
    if vertexflag:
        for v in G['V']:
            plt.plot(float(v[0]), float(v[1]), 'ro')
    
    # Set plot properties
    plt.axis('square')
    plt.draw()
    plt.pause(0.001)  # Add a small pause to allow for plot updates

# Main function
def main():
    # Use the TkAgg backend
    plt.switch_backend('TkAgg')

    # Adjust the figure size
    plt.rcParams['figure.figsize'] = [10, 10]

    # Initialize dynamic maze
    dynamic_maze = DynamicMaze(20, 20)
    
    # Plot the initial maze
    plotgraph(dynamic_maze.maze)
    
    # Get the Tk window and maximize it
    figManager = plt.get_current_fig_manager()
    figManager.window.state('zoomed')
    plt.pause(1)  # Add a small pause to allow for plot updates

    # Main loop
    while True:
        # Update maze
        dynamic_maze.updateMaze(1)  # Update maze every iteration
        plotgraph(dynamic_maze.maze)  # Update the plot

        # Find path
        path = dynamic_maze.findPath()
        print("Path found:", path)

        # Sleep for a while before the next iteration
        # time.sleep(1)

# Execute main function
if __name__ == "__main__":
    main()
