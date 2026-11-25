"""Plain data models shared across the package."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Parcel:
    id: str
    weight: int      # kg
    priority: int    # higher is more important
    deadline: int    # hours until due
    dest: int        # graph node the parcel is delivered to
