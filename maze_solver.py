#!/usr/bin/env python3

from collections import deque

from maze_generator import Cell, Maze


def solve_bfs(
        maze: Maze,
        entry: tuple[int, int],
        exit: tuple[int, int]
) -> str:
    
    entry_cell = maze.get_cell(entry[0], entry[1])
    exit_cell = maze.get_cell(exit[0], exit[1])

    if entry_cell is None:
        raise ValueError("Invalid entry cell")

    if exit_cell is None:
        raise ValueError("Invalid exit cell")

    queue: deque[tuple[Cell, str]] = deque()
    visited: set[tuple[int, int]] = set()

    queue.append((entry_cell, ""))
    visited.add((entry_cell.x, entry_cell.y))

    while queue:
        current, path = queue.popleft()

        if current == exit_cell:
            return path

        for direction, neighbor in get_accessible_neighbors(maze, current):
            coordinates = (neighbor.x, neighbor.y)

            if coordinates in visited:
                continue

            visited.add(coordinates)
            queue.append((neighbor, path + direction))

    raise ValueError("No path found from entry to exit")


def get_accessible_neighbors(
        maze: Maze,
        cell: Cell
) -> list[tuple[str, Cell]]:
    
    neighbors: list[tuple[str, Cell]] = []

    directions: list[tuple[str, int, int, int]] = [
        ("N", 0, -1, Cell.N),
        ("E", 1, 0, Cell.E),
        ("S", 0, 1, Cell.S),
        ("W", -1, 0, Cell.W),
    ]

    for direction_name, dx, dy, wall in directions:
        if cell.has_wall(wall):
            continue

        neighbor = maze.get_cell(cell.x + dx, cell.y + dy)

        if neighbor is None:
            continue

        if neighbor.is_42:
            continue

        neighbors.append((direction_name, neighbor))

    return neighbors