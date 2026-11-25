"""Step 1: prioritise parcels with merge sort. Time O(n log n), space O(n)."""

from typing import Callable, List, Sequence, TypeVar

from .models import Parcel

T = TypeVar("T")


def merge_sort(items: Sequence[T], key: Callable[[T], object] = lambda x: x) -> List[T]:
    """Stable merge sort. Returns a new sorted list."""
    if len(items) < 2:
        return list(items)
    mid = len(items) // 2
    left = merge_sort(items[:mid], key)
    right = merge_sort(items[mid:], key)
    merged: List[T] = []
    i = j = 0
    while i < len(left) and j < len(right):
        if key(right[j]) < key(left[i]):
            merged.append(right[j])
            j += 1
        else:                       # ties keep the left item first, so the sort is stable
            merged.append(left[i])
            i += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def deadline_priority_key(p: Parcel) -> tuple:
    """Earliest deadline first, then highest priority."""
    return (p.deadline, -p.priority)
