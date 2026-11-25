"""Step 2: choose the best load. 0/1 knapsack by dynamic programming, O(n*W)."""

from dataclasses import dataclass
from typing import List, Sequence

from .models import Parcel


@dataclass
class KnapsackResult:
    best: int                 # total priority of the chosen parcels
    picked: List[Parcel]
    table: List[List[int]]    # table[i][w]: best priority using first i parcels, w kg room

    @property
    def weight(self) -> int:
        return sum(p.weight for p in self.picked)


def knapsack(items: Sequence[Parcel], capacity: int) -> KnapsackResult:
    n = len(items)
    table = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        item = items[i - 1]
        for w in range(capacity + 1):
            table[i][w] = table[i - 1][w]                         # skip the parcel
            if item.weight <= w:                                  # or take it
                table[i][w] = max(table[i][w], table[i - 1][w - item.weight] + item.priority)

    picked: List[Parcel] = []
    w = capacity
    for i in range(n, 0, -1):                                     # walk back through the table
        if table[i][w] != table[i - 1][w]:
            picked.append(items[i - 1])
            w -= items[i - 1].weight
    picked.reverse()
    return KnapsackResult(table[n][capacity], picked, table)


def greedy_knapsack(items: Sequence[Parcel], capacity: int) -> List[Parcel]:
    """Greedy by priority per kg. Fast, but not always optimal (compare with knapsack)."""
    chosen, used = [], 0
    for p in sorted(items, key=lambda p: p.priority / p.weight, reverse=True):
        if used + p.weight <= capacity:
            chosen.append(p)
            used += p.weight
    return chosen
