import argparse
import time
import matplotlib.pyplot as plt
from DynamicMaze import DynamicMaze

def main(rows, cols, pawnSpeed, updateFactor):

    # Initialize dynamic maze.
    dynamicMaze = DynamicMaze(rows, cols)
    
    # Plot the initial maze.
    dynamicMaze.plot()

    figManager = plt.get_current_fig_manager()
    figManager.window.state('zoomed')
    # Add a small pause for the windws to be arranged.
    plt.pause(1)
    
    # Normalize pawn speed to ensure it's between 0 and 1.
    pawnSpeed = max(0.0000001, min(1, pawnSpeed))
    
    # Normalize update factor to ensure it's greater than or equal to 1.
    updateFactor = max(0, updateFactor)

    # Calculate the number of cycles between each movement based on pawn speed
    cyclesPerMove = int(1 / pawnSpeed)

    counter = 0
    while True:
        # Update maze and move pawn every cyclesPerMove cycles. Plot the resulting
        # maze and panws position after each update.
        dynamicMaze.updateMaze(updateFactor)
        counter += 1
        if counter % cyclesPerMove == 0:
            dynamicMaze.pawn.move()
        dynamicMaze.plot()

        # Pause briefly to control the simulation speed.
        time.sleep(0.01)

if __name__ == "__main__":
    # Parse command-line arguments.
    parser = argparse.ArgumentParser(description='Dynamic Maze Solver')
    parser.add_argument('--rows', type=int, default=12, help='Number of rows in the maze')
    parser.add_argument('--cols', type=int, default=12, help='Number of columns in the maze')
    parser.add_argument('--pawnSpeed', type=float, default=0.33333, help='Speed of the pawn')
    parser.add_argument('--updateFactor', type=int, default=5, help='Factor of the updates')
    args = parser.parse_args()

    # Call main function with parsed arguments.
    main(args.rows, args.cols, args.pawnSpeed, args.updateFactor)
