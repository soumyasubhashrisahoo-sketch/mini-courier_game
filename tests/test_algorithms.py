from itertools import combinations

from mini_courier.generator import LCG, make_graph, make_parcels
from mini_courier.graph import all_pairs, dijkstra, dijkstra_heap
from mini_courier.knapsack import greedy_knapsack, knapsack
from mini_courier.models import Parcel
from mini_courier.planner import plan_trip
from mini_courier.routing import brute_force, nearest_neighbour, route_length, two_opt
from mini_courier.sorting import deadline_priority_key, merge_sort


def test_merge_sort_matches_builtin_and_is_stable():
    data = [(3, "a"), (1, "b"), (3, "c"), (2, "d"), (1, "e")]
    assert merge_sort(data, key=lambda x: x[0]) == sorted(data, key=lambda x: x[0])


def test_parcels_sorted_by_deadline_then_priority():
    parcels = make_parcels(30, LCG(3), 10)
    out = merge_sort(parcels, deadline_priority_key)
    assert out == sorted(parcels, key=deadline_priority_key)


def test_knapsack_matches_brute_force():
    parcels = make_parcels(10, LCG(5), 10)
    cap = 20
    best = max(
        sum(p.priority for p in c)
        for r in range(len(parcels) + 1)
        for c in combinations(parcels, r)
        if sum(p.weight for p in c) <= cap
    )
    result = knapsack(parcels, cap)
    assert result.best == best
    assert result.weight <= cap
    assert sum(p.priority for p in result.picked) == best


def test_knapsack_beats_or_ties_greedy():
    parcels = make_parcels(14, LCG(7), 10)
    greedy = sum(p.priority for p in greedy_knapsack(parcels, 30))
    assert knapsack(parcels, 30).best >= greedy


def test_dijkstra_versions_agree():
    graph = make_graph(30, LCG(9))
    a, b = dijkstra(graph, 0), dijkstra_heap(graph, 0)
    assert all(abs(x - y) < 1e-9 for x, y in zip(a.dist, b.dist))


def test_path_to_starts_at_source_and_ends_at_target():
    graph = make_graph(10, LCG(7))
    sp = dijkstra(graph, 0)
    path = sp.path_to(7)
    assert path[0] == 0 and path[-1] == 7


def test_two_opt_never_worse_and_brute_force_is_best():
    graph = make_graph(10, LCG(21))
    dist = [sp.dist for sp in all_pairs(graph)]
    stops = [1, 2, 3, 4, 5, 6]
    nn = nearest_neighbour(stops, dist)
    improved = two_opt(nn, dist)
    best = brute_force(stops, dist)
    assert route_length(improved, dist) <= route_length(nn, dist) + 1e-9
    assert route_length(best, dist) <= route_length(improved, dist) + 1e-9


def test_brute_force_refuses_large_inputs():
    assert brute_force(list(range(1, 12)), [[0] * 12] * 12) is None


def test_plan_trip_end_to_end():
    plan = plan_trip(14, 30, 7)
    assert plan.load.weight <= 30
    assert plan.road_nodes[0] == 0 and plan.road_nodes[-1] == 0
    assert plan.two_opt_km <= plan.nn_km + 1e-9
