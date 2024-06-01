import matplotlib.pyplot as plt
from dynamicMaze import DynamicMaze
    
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
    dynamic_maze.plot()

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
        dynamic_maze.plot()

# Execute main function
if __name__ == "__main__":
    main()

