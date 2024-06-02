import argparse
import time
import matplotlib.pyplot as plt
from DynamicMaze import DynamicMaze

# Main function
def main(maze_rows, maze_cols, pawn_speed):
    # Use the TkAgg backend
    plt.switch_backend('TkAgg')

    # Initialize dynamic maze
    dynamic_maze = DynamicMaze(maze_rows, maze_cols)
    
    # Plot the initial maze
    counter = 0
    print("Iteration", counter)
    dynamic_maze.plot()

    # Get the Tk window and maximize it
    figManager = plt.get_current_fig_manager()
    figManager.window.state('zoomed')
    plt.pause(1)  # Add a small pause to allow for plot updates
    
    # Normalize pawn speed to ensure it's between 0 and 1
    pawn_speed = max(0.0000001, min(1, pawn_speed))

    # Calculate the number of iterations between each movement based on pawn speed
    iterations_per_move = int(1 / pawn_speed)

    # Main loop
    while True:
        # Update maze
        dynamic_maze.updateMaze()  # Update maze every iteration
        counter += 1
        if counter % iterations_per_move == 0:
            dynamic_maze.pawn.move()
        print("Iteration", counter)
        dynamic_maze.plot()

        # Pause briefly to control the simulation speed
        time.sleep(0.01)

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Dynamic Maze Solver')
    parser.add_argument('--rows', type=int, default=15, help='Number of rows in the maze')
    parser.add_argument('--cols', type=int, default=15, help='Number of columns in the maze')
    parser.add_argument('--speed', type=float, default=0.1, help='Speed of the pawn (in seconds per move)')
    args = parser.parse_args()

    # Call main function with parsed arguments
    main(args.rows, args.cols, args.speed)
