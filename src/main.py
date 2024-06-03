import argparse
import time
import matplotlib.pyplot as plt
from DynamicMaze import DynamicMaze

# Main function
def main(rows, cols, pawnSpeed, updateFactor):
    # Use the TkAgg backend
    plt.switch_backend('TkAgg')

    # Initialize dynamic maze
    dynamic_maze = DynamicMaze(rows, cols)
    
    # Plot the initial maze
    dynamic_maze.plot()

    # Get the Tk window and maximize it
    figManager = plt.get_current_fig_manager()
    figManager.window.state('zoomed')
    plt.pause(1)  # Add a small pause to allow for plot updates
    
    # Normalize pawn speed to ensure it's between 0 and 1
    pawnSpeed = max(0.0000001, min(1, pawnSpeed))
    
    # Normalize update factor to ensure it's greater than or equal to 1
    updateFactor = max(1, updateFactor)

    # Calculate the number of iterations between each movement based on pawn speed
    iterations_per_move = int(1 / pawnSpeed)

    # Main loop
    counter = 0
    while True:
        # Update maze
        dynamic_maze.updateMaze(updateFactor)  # Update maze every iteration
        counter += 1
        if counter % iterations_per_move == 0:
            dynamic_maze.pawn.move()
        dynamic_maze.plot()

        # Pause briefly to control the simulation speed
        time.sleep(0.01)

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Dynamic Maze Solver')
    parser.add_argument('--rows', type=int, default=12, help='Number of rows in the maze')
    parser.add_argument('--cols', type=int, default=12, help='Number of columns in the maze')
    parser.add_argument('--pawnSpeed', type=float, default=0.33333, help='Speed of the pawn (in seconds per move)')
    parser.add_argument('--updateFactor', type=int, default=15, help='Factor of the updates.')
    args = parser.parse_args()

    # Call main function with parsed arguments
    main(args.rows, args.cols, args.pawnSpeed, args.updateFactor)
