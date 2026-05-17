"""
Visitor Pattern — Operations over Map Elements
==============================================

Use case: a map is made of different element types — Road, Park, River.
The element types rarely change. But we keep needing NEW operations over
them: estimate maintenance cost, render to text, sum up total area, export
to GeoJSON, ...

Visitor is the fit when the object STRUCTURE is stable but the set of
OPERATIONS keeps growing. It lets you add an operation without editing any
element class.
"""

from abc import ABC, abstractmethod


# ============================================================================
# BEFORE — every operation is a method on every element class
# ============================================================================
#
# Pain points:
#   * Adding one new operation (say "render") forces an edit to Road, Park
#     AND River. The number of edits grows with the number of element types.
#   * Each element class accumulates unrelated concerns: geometry, costing,
#     rendering, exporting — all tangled in one class.
#   * Operation logic is scattered across classes; you cannot read the whole
#     "cost" algorithm in one place.


class RoadBefore:
    def __init__(self, length_km: float, lanes: int):
        self.length_km = length_km
        self.lanes = lanes

    def area(self) -> float:
        return self.length_km * 1000 * (self.lanes * 3.5)  # 3.5 m per lane

    def maintenance_cost(self) -> float:
        return self.length_km * self.lanes * 1200

    # Want to add render()? Edit this class — and Park, and River too.


class ParkBefore:
    def __init__(self, area_sqm: float):
        self.area_sqm = area_sqm

    def area(self) -> float:
        return self.area_sqm

    def maintenance_cost(self) -> float:
        return self.area_sqm * 0.5


class RiverBefore:
    def __init__(self, length_km: float, width_m: float):
        self.length_km = length_km
        self.width_m = width_m

    def area(self) -> float:
        return self.length_km * 1000 * self.width_m

    def maintenance_cost(self) -> float:
        return 0.0  # rivers are not maintained


# ============================================================================
# AFTER — elements only "accept" a visitor; operations are visitor classes
# ============================================================================
#
# Each element implements one tiny method: accept(visitor). It calls back the
# visitor's method for its own type ("double dispatch"). An operation is now
# a single class holding the logic for every element type — readable in one
# place, and added without touching any element.


class MapElement(ABC):
    """Base type for anything on the map."""

    @abstractmethod
    def accept(self, visitor: "MapVisitor"):
        """Hand this element to a visitor (double dispatch)."""
        ...


class Road(MapElement):
    def __init__(self, length_km: float, lanes: int):
        self.length_km = length_km
        self.lanes = lanes

    def accept(self, visitor: "MapVisitor"):
        return visitor.visit_road(self)


class Park(MapElement):
    def __init__(self, area_sqm: float):
        self.area_sqm = area_sqm

    def accept(self, visitor: "MapVisitor"):
        return visitor.visit_park(self)


class River(MapElement):
    def __init__(self, length_km: float, width_m: float):
        self.length_km = length_km
        self.width_m = width_m

    def accept(self, visitor: "MapVisitor"):
        return visitor.visit_river(self)


class MapVisitor(ABC):
    """
    The visitor interface: one method per element type. A concrete visitor
    is one whole operation, with its logic for every element in one class.
    """

    @abstractmethod
    def visit_road(self, road: Road):
        ...

    @abstractmethod
    def visit_park(self, park: Park):
        ...

    @abstractmethod
    def visit_river(self, river: River):
        ...


class AreaVisitor(MapVisitor):
    """Operation: compute the surface area (m²) of an element."""

    def visit_road(self, road: Road) -> float:
        return road.length_km * 1000 * (road.lanes * 3.5)

    def visit_park(self, park: Park) -> float:
        return park.area_sqm

    def visit_river(self, river: River) -> float:
        return river.length_km * 1000 * river.width_m


class MaintenanceCostVisitor(MapVisitor):
    """Operation: estimate the yearly maintenance cost of an element."""

    def visit_road(self, road: Road) -> float:
        return road.length_km * road.lanes * 1200

    def visit_park(self, park: Park) -> float:
        return park.area_sqm * 0.5

    def visit_river(self, river: River) -> float:
        return 0.0


class RenderVisitor(MapVisitor):
    """
    Operation: produce a human-readable label. NOTE: adding this whole new
    operation required ZERO changes to Road, Park or River.
    """

    def visit_road(self, road: Road) -> str:
        return f"Road [{road.length_km} km, {road.lanes} lanes]"

    def visit_park(self, park: Park) -> str:
        return f"Park [{park.area_sqm} sqm]"

    def visit_river(self, river: River) -> str:
        return f"River [{river.length_km} km, {river.width_m} m wide]"


# ============================================================================
# Demo
# ============================================================================

if __name__ == "__main__":
    print("--- BEFORE ---")
    before_city = [RoadBefore(5, 2), ParkBefore(20_000), RiverBefore(3, 40)]
    print("Total area:", sum(e.area() for e in before_city), "sqm")
    print("Total cost:", sum(e.maintenance_cost() for e in before_city))

    print("\n--- AFTER ---")
    city: list[MapElement] = [Road(5, 2), Park(20_000), River(3, 40)]

    area = AreaVisitor()
    cost = MaintenanceCostVisitor()
    render = RenderVisitor()

    for element in city:
        print(
            f"{element.accept(render):<35} "
            f"area={element.accept(area):>12,.0f} sqm   "
            f"cost={element.accept(cost):>10,.0f}"
        )

    print("\nTotal area:", sum(e.accept(area) for e in city), "sqm")
    print("Total cost:", sum(e.accept(cost) for e in city))
