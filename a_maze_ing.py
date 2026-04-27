#!/usr/bin/env python3

from maze_generator import MazeGenerator, display_ascii
from maze_solver import solve_bfs


def main() -> None:
    """Generate, solve, display and write a maze."""
    width = 15
    height = 15
    entry = (0, 0)
    exit = (14, 14)
    seed = 42
    perfect = True
    output_file = "maze_output.txt"

    try:
        generator = MazeGenerator(
            width=width,
            height=height,
            entry=entry,
            exit=exit,
            seed=seed,
            perfect=perfect
        )

        maze = generator.generate()
        path = solve_bfs(maze, entry, exit)

        maze.write_hex_file(
            output_file,
            entry,
            exit,
            path
        )

        display_ascii(maze, entry, exit)

        print()
        print(f"Output file: {output_file}")
        print(f"Path: {path}")

    except ValueError as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()