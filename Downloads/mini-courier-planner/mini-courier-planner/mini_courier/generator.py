"""Deterministic random data, so a seed always gives the same city and parcels."""

import math
from typing import List

from .graph import Graph
from .models import Parcel


class LCG:
    """Linear congruential generator (same constants as the web version)."""

    def __init__(self, seed: int) -> None:
        self.state = seed % 2**32

    def random(self) -> float:
        self.state = (self.state * 1664525 + 1013904223) % 2**32
        return self.state / 2**32

    def randint(self, low: int, high: int) -> int:
        """Inclusive integer in [low, high]."""
        return low + int(self.random() * (high - low + 1))


def make_parcels(n: int, rng: LCG, num_nodes: int) -> List[Parcel]:
    return [
        Parcel(
            id=f"P{i + 1}",
            weight=rng.randint(1, 9),
            priority=rng.randint(1, 10),
            deadline=rng.randint(2, 23),
            dest=rng.randint(1, num_nodes - 1),
        )
        for i in range(n)
    ]


def make_graph(num_nodes: int, rng: LCG, neighbours: int = 3) -> Graph:
    """Random points joined by a backbone path plus each point's nearest roads."""
    points = [(40 + rng.random() * 520, 40 + rng.random() * 340) for _ in range(num_nodes)]
    graph = Graph(points)
    for i in range(1, num_nodes):
        graph.add_road(i - 1, i)
    for i in range(num_nodes):
        nearest = sorted(
            (j for j in range(num_nodes) if j != i),
            key=lambda j: math.dist(points[i], points[j]),
        )
        for j in nearest[:neighbours]:
            graph.add_road(i, j)
    return graph
