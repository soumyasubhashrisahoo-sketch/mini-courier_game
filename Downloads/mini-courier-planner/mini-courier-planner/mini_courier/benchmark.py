"""Step 5: measure how each algorithm grows when the input doubles."""

import math
import time
from typing import Callable, Dict, List, Sequence

from .generator import LCG, make_graph
from .graph import dijkstra, dijkstra_heap
from .knapsack import knapsack
from .models import Parcel
from .routing import nearest_neighbour
from .sorting import deadline_priority_key, merge_sort


def _best_of(fn: Callable[[], object], repeats: int = 3) -> float:
    best = math.inf
    for _ in range(repeats):
        start = time.perf_counter()
        fn()
        best = min(best, (time.perf_counter() - start) * 1000)
    return best


def run_benchmark(sizes: Sequence[int] = (100, 200, 400, 800)) -> Dict[str, List[float]]:
    """Milliseconds per algorithm for each size (best of 3)."""
    results: Dict[str, List[float]] = {
        "Merge sort": [], "Knapsack DP (W=50)": [], "Dijkstra array": [],
        "Dijkstra heap": [], "Nearest-neighbour (n/4 stops)": [],
    }
    for n in sizes:
        rng = LCG(11)
        parcels = [Parcel(f"P{i}", rng.randint(1, 9), rng.randint(1, 10), rng.randint(0, 23), 1) for i in range(n)]
        graph = make_graph(n, rng)
        k = n // 4
        pts = [(rng.random() * 500, rng.random() * 500) for _ in range(k + 1)]
        dist = [[math.dist(a, b) for b in pts] for a in pts]
        stops = list(range(1, k + 1))

        results["Merge sort"].append(_best_of(lambda: merge_sort(parcels, deadline_priority_key)))
        results["Knapsack DP (W=50)"].append(_best_of(lambda: knapsack(parcels, 50)))
        results["Dijkstra array"].append(_best_of(lambda: dijkstra(graph, 0)))
        results["Dijkstra heap"].append(_best_of(lambda: dijkstra_heap(graph, 0)))
        results["Nearest-neighbour (n/4 stops)"].append(_best_of(lambda: nearest_neighbour(stops, dist)))
    return results


def format_benchmark(results: Dict[str, List[float]], sizes: Sequence[int]) -> str:
    head = f"{'Step':<32}" + "".join(f"{'n=' + str(n):>16}" for n in sizes)
    lines = [head, "-" * len(head)]
    for name, times in results.items():
        cells = []
        for i, t in enumerate(times):
            ratio = f" (x{t / max(times[i - 1], 0.001):.1f})" if i else ""
            cells.append(f"{t:>8.2f}{ratio:<8}")
        lines.append(f"{name:<32}" + "".join(f"{c:>16}" for c in cells))
    lines.append("\nThe (x) value is the growth from the previous size. Compare it with the Big-O prediction.")
    return "\n".join(lines)
