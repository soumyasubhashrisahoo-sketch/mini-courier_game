"""Step 3: the road map and shortest paths (Dijkstra)."""

import heapq
import math
from dataclasses import dataclass
from typing import List, Tuple

INF = math.inf


class Graph:
    def __init__(self, points: List[Tuple[float, float]]) -> None:
        self.points = points
        self.adj: List[List[Tuple[int, float]]] = [[] for _ in points]

    def __len__(self) -> int:
        return len(self.points)

    def add_road(self, a: int, b: int) -> None:
        if a == b or any(v == b for v, _ in self.adj[a]):
            return
        w = math.dist(self.points[a], self.points[b])
        self.adj[a].append((b, w))
        self.adj[b].append((a, w))


@dataclass
class ShortestPaths:
    dist: List[float]
    prev: List[int]

    def path_to(self, target: int) -> List[int]:
        path, v = [], target
        while v != -1:
            path.append(v)
            v = self.prev[v]
        return path[::-1]


def dijkstra(graph: Graph, source: int) -> ShortestPaths:
    """Array-scan version. Time O(V^2), space O(V)."""
    n = len(graph)
    dist, prev, done = [INF] * n, [-1] * n, [False] * n
    dist[source] = 0.0
    for _ in range(n):
        u = -1
        for i in range(n):
            if not done[i] and (u < 0 or dist[i] < dist[u]):
                u = i
        if u < 0 or dist[u] == INF:
            break
        done[u] = True
        for v, w in graph.adj[u]:                 # relax every road out of u
            if dist[u] + w < dist[v]:
                dist[v], prev[v] = dist[u] + w, u
    return ShortestPaths(dist, prev)


def dijkstra_heap(graph: Graph, source: int) -> ShortestPaths:
    """Binary-heap version. Time O((V + E) log V). Better for large sparse maps."""
    n = len(graph)
    dist, prev = [INF] * n, [-1] * n
    dist[source] = 0.0
    heap = [(0.0, source)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue                               # stale entry
        for v, w in graph.adj[u]:
            if d + w < dist[v]:
                dist[v], prev[v] = d + w, u
                heapq.heappush(heap, (dist[v], v))
    return ShortestPaths(dist, prev)


def all_pairs(graph: Graph) -> List[ShortestPaths]:
    return [dijkstra(graph, s) for s in range(len(graph))]
