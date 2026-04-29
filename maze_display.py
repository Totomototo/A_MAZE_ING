#!/usr/bin/env python3

import os

from mazegen.maze_generator import Cell, Maze, MazeGenerator
from maze_solver import solve_bfs


WALL_COLORS: dict[str, str] = {
    "white": "\033[37m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
}

RESET = "\033[0m"
PATH_COLOR = "\033[32m"
ENTRY_COLOR = "\033[34m"
EXIT_COLOR = "\033[31m"
PATTERN_COLOR = "\033[35m"


def clear_screen() -> None:
    """Clear the terminal screen."""
    os.system("clear")


def path_to_arrows(
        entry: tuple[int, int],
        path: str
) -> dict[tuple[int, int], str]:

    x, y = entry
    arrows: dict[tuple[int, int], str] = {}

    moves: dict[str, tuple[int, int]] = {
        "N": (0, -1),
        "E": (1, 0),
        "S": (0, 1),
        "W": (-1, 0),
    }

    symbols: dict[str, str] = {
        "N": "↑",
        "E": "→",
        "S": "↓",
        "W": "←",
    }

    for direction in path:
        arrows[(x, y)] = symbols[direction]

        dx, dy = moves[direction]
        x += dx
        y += dy

    return arrows


def color_text(text: str, color: str) -> str:
    return f"{color}{text}{RESET}"


def display_ascii(
        maze: Maze,
        entry: tuple[int, int],
        exit: tuple[int, int],
        path: str = "",
        show_path: bool = False,
        wall_color: str = "white"
) -> None:

    path_arrows: dict[tuple[int, int], str] = {}

    if show_path:
        path_arrows = path_to_arrows(entry, path)

    color = WALL_COLORS.get(wall_color, WALL_COLORS["white"])

    print(color_text("+", color), end="")
    for _ in range(maze.width):
        print(color_text("---+", color), end="")
    print()

    for y in range(maze.height):
        print(color_text("|", color), end="")

        for x in range(maze.width):
            cell = maze.grid[y][x]
            pos = (x, y)

            if pos == entry:
                content = color_text(" E ", ENTRY_COLOR)
            elif pos == exit:
                content = color_text(" X ", EXIT_COLOR)
            elif cell.is_42:
                content = color_text(" # ", PATTERN_COLOR)
            elif show_path and pos in path_arrows:
                content = color_text(f" {path_arrows[pos]} ", PATH_COLOR)
            else:
                content = "   "

            print(content, end="")

            if cell.has_wall(Cell.E):
                print(color_text("|", color), end="")
            else:
                print(" ", end="")

        print()

        print(color_text("+", color), end="")
        for x in range(maze.width):
            cell = maze.grid[y][x]

            if cell.has_wall(Cell.S):
                print(color_text("---+", color), end="")
            else:
                print(color_text("   +", color), end="")

        print()


def choose_wall_color(current_color: str) -> str:

    print("\nAvailable colors:")
    for color in WALL_COLORS:
        print(f"- {color}")

    selected = input(
        f"\nCurrent color is {current_color}."
        f" New color: ").strip()

    if selected not in WALL_COLORS:
        print("Invalid color, keeping current color.")
        input("Press Enter to continue...")
        return current_color

    return selected


def regenerate_maze(
        width: int,
        height: int,
        entry: tuple[int, int],
        exit: tuple[int, int],
        seed: int | None,
        perfect: bool
) -> tuple[Maze, str]:

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

    return maze, path


def run_ascii_interface(
        width: int,
        height: int,
        entry: tuple[int, int],
        exit: tuple[int, int],
        seed: int | None,
        perfect: bool
) -> tuple[Maze, str]:

    maze, path = regenerate_maze(
        width,
        height,
        entry,
        exit,
        seed,
        perfect
    )

    show_path = False
    wall_color = "white"
    current_seed = seed

    while True:
        clear_screen()

        print("=== A-Maze-ing ===")
        print(f"Size: {width}x{height}")
        print(f"Entry: {entry}")
        print(f"Exit: {exit}")
        print(f"Perfect: {perfect}")
        print(f"Path visible: {show_path}")
        print(f"Wall color: {wall_color}")
        print(f"Seed: {seed}")
        maze.place_42()
        print()

        display_ascii(
            maze=maze,
            entry=entry,
            exit=exit,
            path=path,
            show_path=show_path,
            wall_color=wall_color
        )

        print("\nCommands:")
        print("1 - Show / hide shortest path")
        print("2 - Regenerate maze")
        print("3 - Change wall color")
        print("4 - Print shortest path")
        print("5 - Quit")

        choice = input("\nChoice: ").strip()

        if choice == "1":
            show_path = not show_path

        elif choice == "2":
            if current_seed is None:
                new_seed = None
            else:
                new_seed = current_seed

            try:
                maze, path = regenerate_maze(
                    width,
                    height,
                    entry,
                    exit,
                    new_seed,
                    perfect
                )
                current_seed = new_seed
            except ValueError as error:
                print(f"Error: {error}")
                input("Press Enter to continue...")

        elif choice == "3":
            wall_color = choose_wall_color(wall_color)

        elif choice == "4":
            print(f"\nShortest path: {path}")
            print(f"Length: {len(path)}")
            input("\nPress Enter to continue...")

        elif choice == "5":
            return maze, path

        else:
            print("Invalid command.")
            input("Press Enter to continue...")
