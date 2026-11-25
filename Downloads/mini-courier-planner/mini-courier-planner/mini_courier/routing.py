"""Step 4: order the stops. Nearest-neighbour, 2-opt improvement and brute force.

`dist` is an all-pairs matrix: dist[a][b] is the road distance from a to b.
Node 0 is the depot. A route is the list of stops between leaving and returning to it.
"""

from itertools import permutations
from typing import List, Optional, Sequence

Matrix = Sequence[Sequence[float]]


def route_length(order: Sequence[int], dist: Matrix) -> float:
    total, cur = 0.0, 0
    for stop in order:
        total += dist[cur][stop]
        cur = stop
    return total + dist[cur][0]


def nearest_neighbour(stops: Sequence[int], dist: Matrix) -> List[int]:
    """Always drive to the closest unvisited stop. Time O(k^2). Not optimal."""
    left, cur, order = list(stops), 0, []
    while left:
        nxt = min(left, key=lambda s: dist[cur][s])
        left.remove(nxt)
        order.append(nxt)
        cur = nxt
    return order


def two_opt(order: Sequence[int], dist: Matrix) -> List[int]:
    """Reverse segments of the route while that makes it shorter (removes crossings)."""
    best = list(order)
    improved = True
    while improved:
        improved = False
        for i in range(len(best) - 1):
            for j in range(i + 1, len(best)):
                cand = best[:i] + best[i:j + 1][::-1] + best[j + 1:]
                if route_length(cand, dist) < route_length(best, dist) - 1e-9:
                    best, improved = cand, True
    return best


def brute_force(stops: Sequence[int], dist: Matrix, limit: int = 8) -> Optional[List[int]]:
    """Try all k! orders. Exact but O(k!), so only for tiny inputs."""
    if len(stops) > limit:
        return None
    return list(min(permutations(stops), key=lambda p: route_length(p, dist), default=()))


def full_path(order: Sequence[int], paths) -> List[int]:
    """Expand a stop order into every road node visited, depot to depot."""
    nodes, cur = [0], 0
    for stop in list(order) + [0]:
        nodes.extend(paths[cur].path_to(stop)[1:])
        cur = stop
    return nodes
