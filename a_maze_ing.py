#!/usr/bin/env python3

import sys

from config_parser import MazeConfig, parse_config_file
from mazegen.maze_generator import Maze, MazeGenerator
from maze_solver import solve_bfs
from maze_display import run_ascii_interface


def generate_and_solve(config: MazeConfig) -> tuple[Maze, str]:

    generator = MazeGenerator(
        width=config.width,
        height=config.height,
        entry=config.entry,
        exit=config.exit,
        seed=config.seed,
        perfect=config.perfect,
    )

    maze = generator.generate()
    path = solve_bfs(maze, config.entry, config.exit)

    return maze, path


def run_project(config: MazeConfig) -> None:

    if config.display and run_ascii_interface is not None:
        maze, path = run_ascii_interface(
            width=config.width,
            height=config.height,
            entry=config.entry,
            exit=config.exit,
            seed=config.seed,
            perfect=config.perfect,
        )
    else:
        maze, path = generate_and_solve(config)

    maze.write_hex_file(
        config.output_file,
        config.entry,
        config.exit,
        path,
    )

    print(f"Maze successfully written to {config.output_file}")
    print(f"Shortest path length: {len(path)}")


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        return

    config_file = sys.argv[1]

    try:
        config = parse_config_file(config_file)
        run_project(config)

    except FileNotFoundError:
        print(f"Error: configuration file not found: {config_file}")

    except PermissionError:
        print(f"Error: permission denied while reading: {config_file}")

    except ValueError as error:
        print(f"Error: {error}")

    except OSError as error:
        print(f"Error: file system error: {error}")


if __name__ == "__main__":
    main()
