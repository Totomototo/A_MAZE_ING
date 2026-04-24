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
        dx:int = other.x - self.x
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
        self.width:int = width
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
            "100010011111",
            "100010000001",
            "111110011111",
            "000010010000",
            "000010011111"
        ]
        pattern_height: int = len(pattern)
        pattern_width: int = len(pattern[0])

        if self.width < pattern_width or self.height < pattern_height:
            print("Error: maze too small to place the 42 pattern")
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
    


class MazeGenerator:
    def __init__(self, width: int, height: int, seed: int | None = None) -> None:
        self.width: int = width
        self.height: int = height
        self.seed: int | None = seed

        self.random = random.Random(seed)
        self.maze = Maze(width, height)

    def generate(self) -> Maze:
        self.maze.place_42()
        start: Cell | None = self.maze.get_cell(0, 0)
        
        if start is None:
            raise ValueError("Maze size must be at least 4x4")
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
            raise ValueError("Generated maze is invalid: some cells are isolated by the 42 pattern")
        
        return self.maze
    
