import enum
from typing import List, Tuple, Set


class Response(enum.Enum):
    HOT = 1
    COLD = 2
    SAME = 3
    EXACT = 4


class Grid:
    def __init__(self, grid: List[List[str]]):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.target_pos = None
        self.prev_pos = None
        self.queries = 0

        for r in range(self.rows):
            for c in range(self.cols):
                if grid[r][c] == "x":
                    self.target_pos = (r, c)
                    break
            if self.target_pos:
                break

    def getResponse(self, row: int, col: int) -> Response:
        """ """
        self.queries += 1

        if row < 0 or row >= self.rows or col < 0 or col >= self.cols:
            raise ValueError(f"Position ({row}, {col}) is out of bounds!")

        current_pos = (row, col)

        if current_pos == self.target_pos:
            return Response.EXACT

        if self.prev_pos is None:
            self.prev_pos = current_pos
            return Response.HOT

        prev_distance = manhattan_distance(self.prev_pos, self.target_pos)
        curr_distance = manhattan_distance(current_pos, self.target_pos)

        self.prev_pos = current_pos

        if curr_distance < prev_distance:
            return Response.HOT
        elif curr_distance > prev_distance:
            return Response.COLD
        else:
            return Response.SAME


def manhattan_distance(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:

    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def findObject(grid_obj: Grid) -> List[int]:

    rows, cols = grid_obj.rows, grid_obj.cols

    curr_row, curr_col = 0, 0

    response = grid_obj.getResponse(curr_row, curr_col)
    if response == Response.EXACT:
        return [curr_row, curr_col]

    candidates = []
    for r in range(rows):
        for c in range(cols):
            if (r, c) != (curr_row, curr_col):
                candidates.append((r, c))

    visited = {(curr_row, curr_col)}

    while candidates:

        next_pos = candidates[len(candidates) // 2]
        next_row, next_col = next_pos

        response = grid_obj.getResponse(next_row, next_col)
        visited.add((next_row, next_col))

        if response == Response.EXACT:
            return [next_row, next_col]

        prev_row, prev_col = curr_row, curr_col
        curr_row, curr_col = next_row, next_col

        if response == Response.HOT:
            candidates = [
                pos
                for pos in candidates
                if pos not in visited
                and manhattan_distance(pos, (curr_row, curr_col))
                < manhattan_distance(pos, (prev_row, prev_col))
            ]
        elif response == Response.COLD:
            candidates = [
                pos
                for pos in candidates
                if pos not in visited
                and manhattan_distance(pos, (curr_row, curr_col))
                > manhattan_distance(pos, (prev_row, prev_col))
            ]
        else:

            candidates = [
                pos
                for pos in candidates
                if pos not in visited
                and manhattan_distance(pos, (curr_row, curr_col))
                == manhattan_distance(pos, (prev_row, prev_col))
            ]

    return gradient_search(grid_obj, curr_row, curr_col, visited)


def gradient_search(
    grid_obj: Grid, start_row: int, start_col: int, visited: Set[Tuple[int, int]]
) -> List[int]:

    rows, cols = grid_obj.rows, grid_obj.cols
    curr_row, curr_col = start_row, start_col

    while True:

        directions = [
            (-1, 0),
            (-1, 1),
            (0, 1),
            (1, 1),
            (1, 0),
            (1, -1),
            (0, -1),
            (-1, -1),
        ]

        best_response = None
        best_pos = None

        for dr, dc in directions:
            next_row, next_col = curr_row + dr, curr_col + dc

            if (
                0 <= next_row < rows
                and 0 <= next_col < cols
                and (next_row, next_col) not in visited
            ):

                response = grid_obj.getResponse(next_row, next_col)
                visited.add((next_row, next_col))

                if response == Response.EXACT:
                    return [next_row, next_col]

                if response == Response.HOT or (best_response is None):
                    best_response = response
                    best_pos = (next_row, next_col)
                    if response == Response.HOT:
                        break

        if best_pos:
            curr_row, curr_col = best_pos
        else:

            for r in range(rows):
                for c in range(cols):
                    if (r, c) not in visited:
                        response = grid_obj.getResponse(r, c)
                        visited.add((r, c))

                        if response == Response.EXACT:
                            return [r, c]

                        curr_row, curr_col = r, c
                        break
                if (r, c) not in visited:
                    break

    return [-1, -1]


def main():

    grid1 = [["o", "o", "o"], ["o", "o", "o"], ["x", "o", "o"]]
    grid_obj1 = Grid(grid1)
    result1 = findObject(grid_obj1)
    print(f"Result: {result1}")

    grid2 = [
        ["o", "o", "o", "o", "o"],
        ["o", "o", "o", "o", "o"],
        ["o", "o", "o", "o", "o"],
        ["o", "o", "o", "o", "o"],
        ["o", "o", "o", "x", "o"],
        ["o", "o", "o", "o", "o"],
    ]
    grid_obj2 = Grid(grid2)
    result2 = findObject(grid_obj2)
    print(f"Result: {result2}")


if __name__ == "__main__":
    main()

    # time complexity is O((rows × cols) × log(rows × cols)) in the worst case
    # space complexity is O(rows × cols).
