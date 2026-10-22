"""Find a minimum-throws route through a Snakes and Ladders board using BFS."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class GameResult:
    """Shortest route from square 1 to the final square."""

    rolls: int
    route: tuple[int, ...]


class SnakeAndLadder:
    """Model a board and solve it as an unweighted graph with BFS.

    Squares are numbered from 1 through ``size``. A move consists of rolling
    one die and then immediately taking any snake or ladder at the landing
    square. A roll that would go beyond the final square is ignored.
    """

    def __init__(
        self,
        size: int = 100,
        jumps: Mapping[int, int] | None = None,
        die_sides: int = 6,
    ) -> None:
        if size < 2:
            raise ValueError("Board size must be at least 2.")
        if die_sides < 1:
            raise ValueError("The die must have at least 1 side.")

        self.size = size
        self.die_sides = die_sides
        self.jumps = dict(jumps or {})
        for start, destination in self.jumps.items():
            if not (1 <= start <= size and 1 <= destination <= size):
                raise ValueError("Every snake and ladder must be on the board.")
            if start == destination:
                raise ValueError("A snake or ladder cannot lead to itself.")

    def shortest_path(self) -> GameResult | None:
        """Return a minimum-throw route, or None if the finish is unreachable."""
        start = self._resolve_jump(1)
        queue: deque[int] = deque([start])
        distance = {start: 0}
        parent: dict[int, int | None] = {start: None}

        while queue:
            square = queue.popleft()
            if square == self.size:
                route: list[int] = []
                current: int | None = square
                while current is not None:
                    route.append(current)
                    current = parent[current]
                route.reverse()
                return GameResult(rolls=distance[square], route=tuple(route))

            for roll in range(1, self.die_sides + 1):
                landing = square + roll
                if landing > self.size:
                    continue
                destination = self._resolve_jump(landing)
                if destination not in distance:
                    distance[destination] = distance[square] + 1
                    parent[destination] = square
                    queue.append(destination)

        return None

    def _resolve_jump(self, square: int) -> int:
        """Follow a snake or ladder at a square, including consecutive jumps."""
        visited: set[int] = set()
        while square in self.jumps:
            if square in visited:
                raise ValueError("Snake/ladder jumps contain a cycle.")
            visited.add(square)
            square = self.jumps[square]
        return square


DEFAULT_JUMPS = {
    # Ladders (bottom -> top)
    4: 14,
    9: 31,
    20: 38,
    28: 84,
    40: 59,
    51: 67,
    63: 81,
    71: 91,
    # Snakes (head -> tail)
    17: 7,
    54: 34,
    62: 19,
    64: 60,
    87: 36,
    93: 73,
    95: 75,
    99: 78,
}


def main() -> None:
    game = SnakeAndLadder(size=100, jumps=DEFAULT_JUMPS)
    result = game.shortest_path()

    print("SNAKE AND LADDER — BFS SHORTEST-PATH SOLVER")
    print("Board: 1 to 100 | Die: 1 to 6")
    print(f"Snakes: {sum(start > end for start, end in DEFAULT_JUMPS.items())}")
    print(f"Ladders: {sum(start < end for start, end in DEFAULT_JUMPS.items())}")
    print()

    if result is None:
        print("The finish cannot be reached with this board setup.")
        return

    print(f"Minimum dice throws: {result.rolls}")
    print("Route after snakes/ladders:")
    print(" -> ".join(map(str, result.route)))
    print("\nEach arrow represents one dice throw, followed by any jump on the landing square.")


if __name__ == "__main__":
    main()