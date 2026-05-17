"""
Template Method Pattern — Trip Report Generator
===============================================

Use case: after a trip the app generates a report. Every report follows the
SAME sequence of steps:
    1. add a header
    2. add the body (the route details)
    3. add a footer
    4. join everything into the final document

Only the FORMATTING of each step changes between output types (plain text,
HTML, Markdown). The skeleton is fixed; the steps vary.

Template Method captures this: a base class defines the fixed algorithm in
one method, and defers the varying steps to subclasses.
"""

from abc import ABC, abstractmethod


# ============================================================================
# BEFORE — each format reimplements the whole sequence
# ============================================================================
#
# Pain points:
#   * The ORDER of steps (header -> body -> footer -> join) is copy-pasted
#     into every class. If the sequence changes, every class must change.
#   * Nothing forces a new format to follow the same skeleton — a developer
#     could easily forget the footer, or join in the wrong order.
#   * The shared structure is invisible: you only see it by reading all
#     three classes and noticing they look alike.


class TextReportBefore:
    def generate(self, destination: str, stops: list[str]) -> str:
        header = f"TRIP REPORT: {destination}"
        body = "Route: " + " -> ".join(stops)
        footer = "-- end of report --"
        return f"{header}\n{body}\n{footer}"


class HtmlReportBefore:
    def generate(self, destination: str, stops: list[str]) -> str:
        header = f"<h1>Trip Report: {destination}</h1>"
        body = "<p>Route: " + " &rarr; ".join(stops) + "</p>"
        footer = "<footer>end of report</footer>"
        return f"{header}\n{body}\n{footer}"


# ============================================================================
# AFTER — the skeleton lives in the base class, steps are overridden
# ============================================================================
#
# `generate()` is the TEMPLATE METHOD: it defines the algorithm once and is
# not meant to be overridden. The abstract step methods are the "holes" that
# each subclass fills in. A new format only supplies the three steps — it
# cannot get the sequence wrong, because it never sees the sequence.


class TripReport(ABC):
    """Defines the fixed report-building algorithm. Subclasses fill the steps."""

    def generate(self, destination: str, stops: list[str]) -> str:
        """
        The template method. The sequence of steps is fixed here and the
        same for every report format.
        """
        parts = [
            self.format_header(destination),
            self.format_body(stops),
            self.format_footer(),
        ]
        return self.join(parts)

    # --- steps that subclasses MUST provide -------------------------------
    @abstractmethod
    def format_header(self, destination: str) -> str:
        ...

    @abstractmethod
    def format_body(self, stops: list[str]) -> str:
        ...

    @abstractmethod
    def format_footer(self) -> str:
        ...

    # --- a step with a sensible default subclasses MAY override -----------
    def join(self, parts: list[str]) -> str:
        """A 'hook': default behaviour, overridable when a format needs it."""
        return "\n".join(parts)


class TextReport(TripReport):
    def format_header(self, destination: str) -> str:
        return f"TRIP REPORT: {destination}"

    def format_body(self, stops: list[str]) -> str:
        return "Route: " + " -> ".join(stops)

    def format_footer(self) -> str:
        return "-- end of report --"


class HtmlReport(TripReport):
    def format_header(self, destination: str) -> str:
        return f"<h1>Trip Report: {destination}</h1>"

    def format_body(self, stops: list[str]) -> str:
        return "<p>Route: " + " &rarr; ".join(stops) + "</p>"

    def format_footer(self) -> str:
        return "<footer>end of report</footer>"


class MarkdownReport(TripReport):
    def format_header(self, destination: str) -> str:
        return f"# Trip Report: {destination}"

    def format_body(self, stops: list[str]) -> str:
        return "**Route:** " + " -> ".join(stops)

    def format_footer(self) -> str:
        return "_end of report_"

    def join(self, parts: list[str]) -> str:
        # Markdown wants a blank line between blocks — overrides the hook.
        return "\n\n".join(parts)


# ============================================================================
# Demo
# ============================================================================

if __name__ == "__main__":
    destination = "Lisbon"
    stops = ["Home", "Airport", "Hotel", "Old Town"]

    print("--- BEFORE ---")
    print(TextReportBefore().generate(destination, stops))
    print()
    print(HtmlReportBefore().generate(destination, stops))

    print("\n--- AFTER ---")
    for report in (TextReport(), HtmlReport(), MarkdownReport()):
        print(f"\n[{type(report).__name__}]")
        print(report.generate(destination, stops))
