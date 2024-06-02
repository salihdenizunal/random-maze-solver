# Random Maze Solver

This is a python project that simulates the dynamic maze generation with time-dependent randomness and pathfinding.

## Overview

The aim of this project is to simulate the dynamic maze environment where the maze walls can disappear and appear randomly. The maze is generated and updated dynamicly. The pawn is trying to navigate from start to the end, with pathfinding algorithms to find the path through the changing maze. The random number generation methods, Prim's algorithm, a mechanism to add and remove random walls, A* algorithm to find the optimal path from enterence to exit is utilized in this project. Various algorithms and data structures are used to implement this functionality.

## Features

- Maze generation with Prim's Maze algorithm, utilizing random number generator lcg2.
- Dynamic maze mechanisim to add and remove the walls.
- Path finding algorithms to find the shortest path from the starting point to the goal.
- Adaptaion of the changing maze environment while finding the path.
- Visualization of the maze environment and pawn movement.

## Installation

To install the project, follow these steps:

1. Clone the repository to your local machine:

git clone https://github.com/your_username/dynamic-maze-solver.git

## Requirements

- Python 3.x
- Matplotlib
- Numpy

Install the required dependencies using pip:

pip install -r requirements.txt

## Usage

To run the simulation, execute the `main.py` script with optional command-line arguments:

python main.py [--rows ROWS] [--cols COLS] [--speed SPEED]

- `--rows ROWS`: Number of rows in the maze (default: 20).
- `--cols COLS`: Number of columns in the maze (default: 20).
- `--speed SPEED`: Speed of the pawn movement (between 0 and 1, default: 0.1).

Example usage:

python main.py --rows 15 --cols 15 --speed 0.2

This will start the simulation of the dynamic maze environment.

## Acknowledgements

- This project was inspired by MMI 513 Term Project, Spring 2024.
