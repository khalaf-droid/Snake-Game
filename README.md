# Snake AI Game

A classic Snake game implemented in Python using Pygame, featuring an AI assistant that uses A* pathfinding algorithm to provide hints for optimal moves.

## Description

This project is a modern take on the classic Snake game where the player controls a snake to eat food and grow longer. The game includes an AI component that calculates the shortest path to the food using the A* algorithm, displaying yellow hint dots to guide the player. The game wraps around the screen edges and includes collision detection.

## Features

- Classic Snake gameplay with smooth controls
- AI-powered pathfinding hints using A* algorithm
- Score tracking
- Game over and restart functionality
- Visual grid for better gameplay
- Toggleable AI hints
- Screen wrapping (snake can go through edges)

## Requirements

- Python 3.x
- Pygame library

## Installation

1. Ensure Python 3.x is installed on your system.
2. Install Pygame using pip:

```bash
pip install pygame
```

## How to Run

Run the game by executing the Python script:

```bash
python snake_curses.py
```

## Controls

- **Arrow Keys**: Move the snake (Up, Down, Left, Right)
- **H**: Toggle AI hints on/off
- **R**: Restart the game when game over

## AI Explanation

The AI uses the A* pathfinding algorithm to find the optimal path from the snake's head to the food. The algorithm considers:

- **g(n)**: The actual cost from the start position to the current position
- **h(n)**: The estimated distance to the food using Manhattan distance
- **f(n) = g(n) + h(n)**: The total cost used for path prioritization

The AI treats the snake's body as obstacles and avoids collisions. Yellow dots show the calculated path when hints are enabled.

## Diagrams

### Game Layout
```
+---------------------+
|                     |
|   +---+---+---+     |
|   | H | B | B |     |
|   +---+---+---+     |
|                     |
|         *           |
|                     |
+---------------------+
```
- **H**: Snake Head (Blue)
- **B**: Snake Body (Dark Green)
- **\***: Food (Red)
- Grid lines are shown in gray

### A* Algorithm Flowchart
```
Start
  |
  v
Initialize Open List (PriorityQueue) with start node
Initialize Closed List (set)
  |
  v
While Open List is not empty:
  |
  v
  Get node with lowest f(n) from Open List
  |
  v
  If node is goal (food position):
  |     |
  |     v
  |   Reconstruct path by backtracking parents
  |     |
  |     v
  |   Return path
  |
  v
  Add current node to Closed List
  |
  v
  For each neighbor (up, down, left, right):
  |     |
  |     v
  |   If neighbor is within bounds and not obstacle:
  |     |
  |     v
  |     Calculate g(n) = current.g + 1
  |     Calculate h(n) = Manhattan distance to goal
  |     Calculate f(n) = g(n) + h(n)
  |     |
  |     v
  |     If neighbor not in Open/Closed or better path:
  |       |
  |       v
  |       Add/Update neighbor in Open List
  |
  v
No path found - Return empty list
```

## Game Mechanics

- The snake starts with length 3 in the center of the screen
- Eating food increases the score by 10 and grows the snake by 1 segment
- The game ends if the snake collides with itself
- The screen wraps around, allowing continuous movement

## Code Structure

- `Node`: Represents a position in the grid for A* pathfinding
- `Snake`: Manages snake position, movement, and rendering
- `Food`: Handles food placement and rendering
- `GameAI`: Implements A* algorithm for pathfinding
- `main()`: Contains the game loop and event handling

## License

This project is open source and available under the MIT License.