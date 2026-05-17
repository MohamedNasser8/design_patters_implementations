"""
Strategy Pattern — Route Planner
================================

Use case: a map app computes a route between two points. The user picks a
travel mode (car, bike, walking). Each mode follows different rules:
  - cars use highways and avoid pedestrian-only paths
  - bikes prefer bike lanes and avoid highways
  - walking takes the shortest path and ignores one-way restrictions

The route-planning ALGORITHM varies; everything around it (taking input,
showing the result) stays the same. That is the textbook fit for Strategy:
a family of interchangeable algorithms, selected at runtime.
"""

# ============================================================================
# BEFORE — one method with a branch per travel mode
# ============================================================================
#
# Pain points:
#   * calculate_route() must be edited every time a new mode is added (it
#     violates the Open/Closed Principle).
#   * All the unrelated algorithms live in one method — a bug in the bike
#     branch sits right next to the car logic.
#   * The travel mode is a magic string; a typo silently falls through.


class RoutePlannerBefore:
    def calculate_route(self, start: str, end: str, mode: str) -> list[str]:
        if mode == "car":
            print("Routing for a car: highways allowed, pedestrian paths skipped")
            return [start, "Highway 7", "Exit 12", end]

        elif mode == "bike":
            print("Routing for a bike: bike lanes preferred, highways avoided")
            return [start, "River bike lane", "Park path", end]

        elif mode == "walking":
            print("Routing for walking: shortest path, one-way streets ignored")
            return [start, "Market Street", "Alley", end]

        else:
            # Adding "transit" or "scooter" means another branch right here.
            raise ValueError(f"Unknown travel mode: {mode}")


# ============================================================================
# AFTER — each algorithm is its own Strategy class
# ============================================================================
#
# RouteStrategy is the common interface. Each concrete strategy encapsulates
# one routing algorithm. RoutePlanner (the "context") holds a strategy and
# delegates to it, knowing nothing about which one it has.
#
# Adding a new mode = adding a new class. No existing code is touched.

from abc import ABC, abstractmethod


class RouteStrategy(ABC):
    """The interface every routing algorithm must implement."""

    @abstractmethod
    def build_route(self, start: str, end: str) -> list[str]:
        ...


class CarRoute(RouteStrategy):
    """Fast roads: highways allowed, pedestrian-only paths skipped."""

    def build_route(self, start: str, end: str) -> list[str]:
        print("Routing for a car: highways allowed, pedestrian paths skipped")
        return [start, "Highway 7", "Exit 12", end]


class BikeRoute(RouteStrategy):
    """Bike lanes preferred, highways avoided."""

    def build_route(self, start: str, end: str) -> list[str]:
        print("Routing for a bike: bike lanes preferred, highways avoided")
        return [start, "River bike lane", "Park path", end]


class WalkingRoute(RouteStrategy):
    """Shortest path; one-way restrictions do not apply to pedestrians."""

    def build_route(self, start: str, end: str) -> list[str]:
        print("Routing for walking: shortest path, one-way streets ignored")
        return [start, "Market Street", "Alley", end]


class RoutePlanner:
    """
    The context. It is configured with a strategy and delegates the actual
    routing to it. The planner never needs an `if mode == ...` branch.
    """

    def __init__(self, strategy: RouteStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: RouteStrategy) -> None:
        """Swap the algorithm at runtime — e.g. when the user changes mode."""
        self._strategy = strategy

    def calculate_route(self, start: str, end: str) -> list[str]:
        return self._strategy.build_route(start, end)


# ============================================================================
# Client
# ============================================================================

if __name__ == "__main__":
    print("--- BEFORE ---")
    before = RoutePlannerBefore()
    print(before.calculate_route("Home", "Office", "car"))
    print(before.calculate_route("Home", "Office", "bike"))

    print("\n--- AFTER ---")
    planner = RoutePlanner(CarRoute())
    print(planner.calculate_route("Home", "Office"))

    # The user switches travel mode — just swap the strategy.
    planner.set_strategy(WalkingRoute())
    print(planner.calculate_route("Home", "Office"))
