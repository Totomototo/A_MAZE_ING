#!/usr/bin/env python3

import random


class Cell:
    N = 1
    E = 2
    S = 4
    W = 8

    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y
        self.walls: int = Cell.N | Cell.E | Cell.S | Cell.W
        self.visited: bool = False
        self.is_42: bool = False

    def remove_wall(self, other: "Cell") -> None:
        dx: int = other.x - self.x
        dy: int = other.y - self.y

        if dx == 1 and dy == 0:
            self.walls &= ~Cell.E
            other.walls &= ~Cell.W

        elif dx == -1 and dy == 0:
            self.walls &= ~Cell.W
            other.walls &= ~Cell.E

        elif dx == 0 and dy == 1:
            self.walls &= ~Cell.S
            other.walls &= ~Cell.N

        elif dx == 0 and dy == -1:
            self.walls &= ~Cell.N
            other.walls &= ~Cell.S

        else:
            raise ValueError("Cells are not adjacent")

    def has_wall(self, direction: int) -> bool:
        return (self.walls & direction) != 0

    def to_hex(self) -> str:
        return format(self.walls, "X")


class Maze:
    def __init__(self, width: int, height: int) -> None:

        if width <= 0 or height <= 0:
            raise ValueError("Maze dimensions must be positive")

        self.width: int = width
        self.height: int = height

        self.grid: list[list[Cell]] = [
            [Cell(x, y) for x in range(width)]
            for y in range(height)
        ]

    def is_inside(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def get_cell(self, x: int, y: int) -> Cell | None:
        if self.is_inside(x, y):
            return self.grid[y][x]
        return None

    def get_neighbors(self, cell: Cell) -> list[Cell]:
        neighbors: list[Cell] = []
        directions: list[tuple[int, int]] = [
            (0, -1),
            (1, 0),
            (0, 1),
            (-1, 0)
        ]

        for dx, dy in directions:
            nx: int = cell.x + dx
            ny: int = cell.y + dy

            if self.is_inside(nx, ny):
                neighbors.append(self.grid[ny][nx])

        return neighbors

    def get_unvisited_neighbors(self, cell: Cell) -> list[Cell]:
        neighbors: list[Cell] = self.get_neighbors(cell)

        return [
            n for n in neighbors
            if not n.visited and not n.is_42
        ]

    def place_42(self) -> bool:
        pattern: list[str] = [
            "10010111",
            "10010001",
            "11110111",
            "00010100",
            "00010111"
        ]
        pattern_height: int = len(pattern)
        pattern_width: int = len(pattern[0])

        if self.width < pattern_width + 2 or self.height < pattern_height + 2:
            print("Maze too small to place the 42")
            return False

        start_x: int = (self.width - pattern_width) // 2
        start_y: int = (self.height - pattern_height) // 2

        for y in range(pattern_height):
            for x in range(pattern_width):
                if pattern[y][x] == "1":
                    cell: Cell = self.grid[start_y + y][start_x + x]
                    cell.is_42 = True
                    cell.walls = Cell.N | Cell.E | Cell.S | Cell.W

        return True

    def no_isolate(self) -> bool:
        for row in self.grid:
            for cell in row:
                if not cell.is_42 and not cell.visited:
                    return False
        return True

    def write_hex_file(
            self,
            filename: str,
            entry: tuple[int, int],
            exit: tuple[int, int],
            path: str = ""
    ) -> None:
        with open(filename, "w") as f:

            for row in self.grid:
                line = ""
                for cell in row:
                    line += cell.to_hex()
                f.write(line + "\n")

            f.write("\n")
            f.write(f"{entry[0]},{entry[1]}\n")
            f.write(f"{exit[0]},{exit[1]}\n")
            f.write(path + "\n")

    def has_open_3x3_area(self) -> bool:
        for y in range(self.height - 2):
            for x in range(self.width - 2):
                if self.is_3x3_fully_open(x, y):
                    return True
        return False

    def is_3x3_fully_open(self, start_x: int, start_y: int) -> bool:
        for y in range(start_y, start_y + 3):
            for x in range(start_x, start_x + 3):
                cell = self.grid[y][x]

                if cell.is_42:
                    return False

                if x < start_x + 2:
                    right = self.grid[y][x + 1]
                    if cell.has_wall(Cell.E) or right.has_wall(Cell.W):
                        return False

                if y < start_y + 2:
                    down = self.grid[y + 1][x]
                    if cell.has_wall(Cell.S) or down.has_wall(Cell.N):
                        return False

        return True

    def would_create_3x3(self, cell: Cell, neighbor: Cell) -> bool:
        original_cell_walls = cell.walls
        original_neighbor_walls = neighbor.walls

        cell.remove_wall(neighbor)

        result = self.has_open_3x3_area()

        cell.walls = original_cell_walls
        neighbor.walls = original_neighbor_walls

        return result

    def walls_are_consistent(self) -> bool:
        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y][x]

                if x < self.width - 1:
                    right = self.grid[y][x + 1]

                    if cell.has_wall(Cell.E) != right.has_wall(Cell.W):
                        return False

                if y < self.height - 1:
                    down = self.grid[y + 1][x]

                    if cell.has_wall(Cell.S) != down.has_wall(Cell.N):
                        return False

        return True

    def outer_walls_ok(self) -> bool:

        for x in range(self.width):
            if not self.grid[0][x].has_wall(Cell.N):
                return False

            if not self.grid[self.height - 1][x].has_wall(Cell.S):
                return False

        for y in range(self.height):

            if not self.grid[y][0].has_wall(Cell.W):
                return False

            if not self.grid[y][self.width - 1].has_wall(Cell.E):
                return False

        return True


class MazeGenerator:
    def __init__(
            self,
            width: int,
            height: int,
            entry: tuple[int, int],
            exit: tuple[int, int],
            seed: int | None = None,
            perfect: bool = True
    ) -> None:

        self.width: int = width
        self.height: int = height
        self.seed: int | None = seed
        self.entry: tuple[int, int] = entry
        self.exit: tuple[int, int] = exit
        self.perfect: bool = perfect

        self.random = random.Random(seed)
        self.maze = Maze(width, height)

    def validate_entry_exit(self) -> None:
        entry_x, entry_y = self.entry
        exit_x, exit_y = self.exit

        if not self.maze.is_inside(entry_x, entry_y):
            raise ValueError("Entry is outside maze bounds")

        if not self.maze.is_inside(exit_x, exit_y):
            raise ValueError("Exit is outside maze bounds")

        if self.entry == self.exit:
            raise ValueError("Entry and exit must be different")

        entry_cell = self.maze.get_cell(entry_x, entry_y)
        exit_cell = self.maze.get_cell(exit_x, exit_y)

        if entry_cell is None or exit_cell is None:
            raise ValueError("Invalid entry or exit")

        if entry_cell.is_42:
            raise ValueError("Entry cannot be inside the 42 pattern")

        if exit_cell.is_42:
            raise ValueError("Exit cannot be inside the 42 pattern")

    def generate(self) -> Maze:
        self.maze.place_42()
        self.validate_entry_exit()
        entry_x, entry_y = self.entry
        start: Cell | None = self.maze.get_cell(entry_x, entry_y)

        if start is None:
            raise ValueError("Invalid entry")
        start.visited = True
        stack: list[Cell] = [start]

        while stack:
            current: Cell = stack[-1]

            neighbors: list[Cell] = self.maze.get_unvisited_neighbors(current)

            if neighbors:
                next_cell: Cell = self.random.choice(neighbors)

                current.remove_wall(next_cell)

                next_cell.visited = True
                stack.append(next_cell)
            else:
                stack.pop()

        if not self.maze.no_isolate():
            raise ValueError(
                "Generated maze is invalid: some normal cells are isolated"
                )

        exit_x, exit_y = self.exit
        exit_cell = self.maze.get_cell(exit_x, exit_y)

        if exit_cell is None or not exit_cell.visited:
            raise ValueError("Exit is unreachable from entry")

        if not self.perfect:
            self.add_loops()

        for row in self.maze.grid:
            for cell in row:
                cell.visited = False

        if not self.maze.walls_are_consistent():
            raise ValueError("Walls are inconsistent")
        if not self.maze.outer_walls_ok():
            raise ValueError("Outer walls are invalid")

        return self.maze

    def has_wall_between(self, cell: Cell, neighbor: Cell) -> bool:
        dx = neighbor.x - cell.x
        dy = neighbor.y - cell.y

        if dx == 1 and dy == 0:
            return cell.has_wall(Cell.E) and neighbor.has_wall(Cell.W)

        if dx == -1 and dy == 0:
            return cell.has_wall(Cell.W) and neighbor.has_wall(Cell.E)

        if dx == 0 and dy == 1:
            return cell.has_wall(Cell.S) and neighbor.has_wall(Cell.N)

        if dx == 0 and dy == -1:
            return cell.has_wall(Cell.N) and neighbor.has_wall(Cell.S)

        return False

    def add_loops(self, ratio: float = 0.08) -> None:
        candidates: list[tuple[Cell, Cell]] = []

        for y in range(self.height):
            for x in range(self.width):
                cell = self.maze.grid[y][x]

                if cell.is_42:
                    continue

                neighbors = self.maze.get_neighbors(cell)

                for neighbor in neighbors:

                    if neighbor.is_42:
                        continue

                    if neighbor.x < cell.x or neighbor.y < cell.y:
                        continue

                    if self.has_wall_between(cell, neighbor):
                        candidates.append((cell, neighbor))

        self.random.shuffle(candidates)

        if not candidates:
            return

        walls_to_down = max(1, int(len(candidates) * ratio))
        opened = 0

        for cell, neighbor in candidates:
            if opened >= walls_to_down:
                break
            if not self.maze.would_create_3x3(cell, neighbor):
                cell.remove_wall(neighbor)
                opened += 1
