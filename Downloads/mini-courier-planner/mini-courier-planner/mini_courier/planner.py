"""Ties the four steps together into one delivery plan."""

from dataclasses import dataclass
from typing import List, Optional

from .generator import LCG, make_graph, make_parcels
from .graph import all_pairs
from .knapsack import KnapsackResult, greedy_knapsack, knapsack
from .models import Parcel
from .routing import brute_force, full_path, nearest_neighbour, route_length, two_opt
from .sorting import deadline_priority_key, merge_sort


@dataclass
class TripPlan:
    parcels: List[Parcel]
    sorted_parcels: List[Parcel]
    capacity: int
    load: KnapsackResult
    greedy_priority: int
    stops: List[int]
    nn_order: List[int]
    nn_km: float
    two_opt_order: List[int]
    two_opt_km: float
    best_order: Optional[List[int]]
    best_km: Optional[float]
    road_nodes: List[int]


def plan_trip(n_parcels: int = 14, capacity: int = 30, seed: int = 7, num_nodes: int = 10) -> TripPlan:
    rng = LCG(seed or 1)
    graph = make_graph(num_nodes, rng)
    parcels = make_parcels(n_parcels, rng, num_nodes)

    ordered = merge_sort(parcels, key=deadline_priority_key)          # step 1
    load = knapsack(ordered, capacity)                                # step 2
    greedy = sum(p.priority for p in greedy_knapsack(ordered, capacity))

    paths = all_pairs(graph)                                          # step 3
    dist = [sp.dist for sp in paths]
    stops = sorted({p.dest for p in load.picked})

    nn = nearest_neighbour(stops, dist)                               # step 4
    improved = two_opt(nn, dist)
    best = brute_force(stops, dist)
    return TripPlan(
        parcels, ordered, capacity, load, greedy, stops,
        nn, route_length(nn, dist), improved, route_length(improved, dist),
        best, route_length(best, dist) if best is not None else None,
        full_path(improved, paths),
    )


def _arrow(order) -> str:
    return "Depot -> " + " -> ".join(map(str, order)) + " -> Depot"


def format_report(plan: TripPlan) -> str:
    out = ["=== 1. Parcels sorted by deadline (merge sort) ==="]
    chosen = {p.id for p in plan.load.picked}
    out.append(f"{'':2}{'id':<5}{'kg':>3}{'pri':>5}{'due h':>7}{'stop':>6}")
    for p in plan.sorted_parcels:
        mark = "*" if p.id in chosen else " "
        out.append(f"{mark} {p.id:<5}{p.weight:>3}{p.priority:>5}{p.deadline:>7}{p.dest:>6}")
    out += [
        "",
        "=== 2. Van load (0/1 knapsack DP) ===",
        f"Loaded {len(plan.load.picked)} of {len(plan.parcels)} parcels, "
        f"{plan.load.weight}/{plan.capacity} kg, total priority {plan.load.best}",
        f"Greedy by priority per kg would only reach {plan.greedy_priority}",
        "",
        "=== 3 and 4. Route (Dijkstra distances) ===",
        f"Stops to visit: {plan.stops}",
        f"Nearest-neighbour: {_arrow(plan.nn_order)}  ({plan.nn_km:.0f} km)",
        f"After 2-opt:       {_arrow(plan.two_opt_order)}  ({plan.two_opt_km:.0f} km)",
    ]
    if plan.best_order is not None:
        out.append(f"Best (all orders): {_arrow(plan.best_order)}  ({plan.best_km:.0f} km)")
    else:
        out.append("Best (all orders): skipped, too many stops for brute force")
    out.append("(* = loaded in the van)")
    return "\n".join(out)
