#%% 
import matplotlib.pyplot as plt
from dynamicMaze import DynamicMaze
import time
import numpy as np

# Function to plot the maze graph
def plotgraph(G, path = None, vertexflag=False):
    # Clear the previous plot
    plt.clf()
    
    # Plot the walls of the maze
    for e in G['W']:
        vec = np.array([e[1][0]-e[0][0], e[1][1]-e[0][1]])
        ort = np.array([-vec[1], vec[0]])
        olen = np.linalg.norm(ort)
        ort = ort / olen
        sum = np.array([(e[1][0]+e[0][0])/2, (e[1][1]+e[0][1])/2])
        startp = sum - ort / 2
        endp = sum + ort / 2
        plt.plot((startp[0], endp[0]), (startp[1], endp[1]), 'gray', linewidth=10)
    
    # Plot the vertices of the maze if vertexflag is True
    if vertexflag:
        for v in G['V']:
            plt.plot(float(v[0]), float(v[1]), 'ro')
    
    # Plot the path if provided
    if path:
        path_coords = [G['V'][i] for i in path]
        path_x = [coord[0] for coord in path_coords]
        path_y = [coord[1] for coord in path_coords]
        plt.plot(path_x, path_y, 'b', linewidth=2)

    # Plot start marker 
    start_coords = G['V'][path[0]]
    plt.plot(start_coords[0], start_coords[1], 'go', markersize=10)

     # Plot finish flag
    end_coords = G['V'][path[-1]]
    flag_x = end_coords[0] + 0.2
    flag_y = end_coords[1] + 0.7  # Adjust the flag height
    plt.plot([end_coords[0], end_coords[0]], [end_coords[1] + 0.5, end_coords[1] ], color='black', linewidth=3)  # Plot flagpole
    plt.plot(flag_x, flag_y, marker='>', color='r', markersize=12)  # Plot flag with triangle facing right

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
    dynamic_maze = DynamicMaze(15, 15)
    
    # Plot the initial maze
    counter = 0
    print("Iteration %d", counter)
    plotgraph(dynamic_maze.maze, dynamic_maze.path)

    # Get the Tk window and maximize it
    figManager = plt.get_current_fig_manager()
    figManager.window.state('zoomed')
    plt.pause(1)  # Add a small pause to allow for plot updates

    # Main loop
    while True:
        # Update maze
        dynamic_maze.updateMaze()  # Update maze every iteration
        counter += 1
        if counter % 3 == 0:
            dynamic_maze.move()
        print("Iteration %d",counter)
        # Find path
        plotgraph(dynamic_maze.maze, dynamic_maze.path)

# Execute main function
if __name__ == "__main__":
    main()

# %%
